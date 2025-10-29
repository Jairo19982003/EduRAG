"""
Evaluations Router - Material evaluation system for Telegram bot
Handles AI-powered grading of student materials
"""

from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from decimal import Decimal
import logging
from datetime import datetime

from app.core.database import get_supabase_client

logger = logging.getLogger(__name__)
router = APIRouter()


# ============================================================================
# MODELS
# ============================================================================

class EvaluationCreate(BaseModel):
    """Model for creating a new evaluation"""
    material_id: str  # UUID as string
    evaluated_by: Optional[str] = None  # Telegram username
    score: float = Field(..., ge=0, le=10, description="Score from 0 to 10")
    coherence_score: Optional[float] = Field(None, ge=0, le=10)
    structure_score: Optional[float] = Field(None, ge=0, le=10)
    strengths: List[str] = Field(default_factory=list)
    improvements: List[str] = Field(default_factory=list)
    ai_model: str = "gpt-4o-mini"
    ai_analysis: Optional[Dict] = None
    pdf_type: Optional[str] = None  # 'digital' or 'scanned'
    ocr_confidence: Optional[float] = None


class EvaluationResponse(BaseModel):
    """Model for evaluation response"""
    id: str
    material_id: str
    evaluated_by: Optional[str]
    score: float
    coherence_score: Optional[float]
    structure_score: Optional[float]
    strengths: List[str]
    improvements: List[str]
    ai_model: str
    pdf_type: Optional[str]
    evaluated_at: datetime
    created_at: datetime


class PendingMaterial(BaseModel):
    """Model for pending material"""
    material_id: str
    title: str
    course_name: str
    uploaded_at: datetime
    file_url: Optional[str]
    processing_status: str


class EvaluationStats(BaseModel):
    """Model for evaluation statistics"""
    total_evaluations: int
    avg_score: float
    total_pending: int
    evaluations_today: int
    avg_coherence: Optional[float]
    avg_structure: Optional[float]


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/pending", response_model=List[PendingMaterial])
async def get_pending_materials(
    limit: int = 50,
    course_id: Optional[str] = None
):
    """
    Obtiene materiales pendientes de evaluación
    
    Args:
        limit: Número máximo de materiales a retornar
        course_id: Filtrar por curso específico (opcional)
    
    Returns:
        Lista de materiales pendientes de calificar
    """
    try:
        supabase = get_supabase_client()
        
        # Query base
        query = supabase.rpc(
            'get_pending_evaluations',
            {'limit_count': limit}
        )
        
        result = query.execute()
        
        # Filtrar por curso si se especifica
        materials = result.data
        if course_id and materials:
            # Necesitamos hacer otra query para filtrar por curso
            materials = [m for m in materials if m.get('course_id') == course_id]
        
        return materials
        
    except Exception as e:
        logger.error(f"Error fetching pending materials: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch pending materials: {str(e)}"
        )


@router.post("/", response_model=EvaluationResponse, status_code=201)
async def create_evaluation(evaluation: EvaluationCreate):
    """
    Crea una nueva evaluación para un material
    
    Args:
        evaluation: Datos de la evaluación
    
    Returns:
        Evaluación creada
    """
    try:
        supabase = get_supabase_client()
        
        # Verificar que el material existe
        material_check = supabase.table("materials").select("id, title").eq("id", evaluation.material_id).execute()
        
        if not material_check.data:
            raise HTTPException(
                status_code=404,
                detail=f"Material with ID {evaluation.material_id} not found"
            )
        
        # Verificar si ya tiene evaluación (opcional: permitir re-evaluación)
        existing = supabase.table("material_evaluations").select("id").eq("material_id", evaluation.material_id).execute()
        
        if existing.data:
            logger.warning(f"Material {evaluation.material_id} already has an evaluation. Creating new one.")
        
        # Crear evaluación
        evaluation_data = {
            "material_id": evaluation.material_id,
            "evaluated_by": evaluation.evaluated_by,
            "score": float(evaluation.score),
            "coherence_score": float(evaluation.coherence_score) if evaluation.coherence_score else None,
            "structure_score": float(evaluation.structure_score) if evaluation.structure_score else None,
            "strengths": evaluation.strengths,
            "improvements": evaluation.improvements,
            "ai_model": evaluation.ai_model,
            "ai_analysis": evaluation.ai_analysis,
            "pdf_type": evaluation.pdf_type,
            "ocr_confidence": float(evaluation.ocr_confidence) if evaluation.ocr_confidence else None
        }
        
        result = supabase.table("material_evaluations").insert(evaluation_data).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to create evaluation")
        
        # Actualizar status del material
        supabase.table("materials").update({
            "evaluation_status": "evaluated"
        }).eq("id", evaluation.material_id).execute()
        
        logger.info(f"Created evaluation for material {evaluation.material_id} with score {evaluation.score}")
        
        return result.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating evaluation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create evaluation: {str(e)}"
        )


@router.get("/material/{material_id}", response_model=EvaluationResponse)
async def get_material_evaluation(material_id: str):
    """
    Obtiene la evaluación de un material específico
    
    Args:
        material_id: ID del material
    
    Returns:
        Evaluación del material
    """
    try:
        supabase = get_supabase_client()
        
        result = supabase.table("material_evaluations").select("*").eq("material_id", material_id).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=404,
                detail=f"No evaluation found for material {material_id}"
            )
        
        # Retornar la evaluación más reciente si hay múltiples
        return result.data[-1] if isinstance(result.data, list) else result.data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching evaluation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch evaluation: {str(e)}"
        )


@router.get("/stats", response_model=EvaluationStats)
async def get_evaluation_statistics():
    """
    Obtiene estadísticas globales de evaluaciones
    
    Returns:
        Estadísticas de evaluaciones
    """
    try:
        supabase = get_supabase_client()
        
        result = supabase.rpc('get_evaluation_stats').execute()
        
        if not result.data:
            # Retornar estadísticas vacías si no hay datos
            return {
                "total_evaluations": 0,
                "avg_score": 0.0,
                "total_pending": 0,
                "evaluations_today": 0,
                "avg_coherence": 0.0,
                "avg_structure": 0.0
            }
        
        return result.data[0] if isinstance(result.data, list) else result.data
        
    except Exception as e:
        logger.error(f"Error fetching statistics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch statistics: {str(e)}"
        )


@router.delete("/{evaluation_id}", status_code=204)
async def delete_evaluation(evaluation_id: str):
    """
    Elimina una evaluación (solo para correcciones)
    
    Args:
        evaluation_id: ID de la evaluación a eliminar
    """
    try:
        supabase = get_supabase_client()
        
        # Obtener material_id antes de eliminar
        eval_data = supabase.table("material_evaluations").select("material_id").eq("id", evaluation_id).execute()
        
        if not eval_data.data:
            raise HTTPException(
                status_code=404,
                detail=f"Evaluation {evaluation_id} not found"
            )
        
        material_id = eval_data.data[0]["material_id"]
        
        # Eliminar evaluación
        supabase.table("material_evaluations").delete().eq("id", evaluation_id).execute()
        
        # Actualizar status del material a pending
        supabase.table("materials").update({
            "evaluation_status": "pending"
        }).eq("id", material_id).execute()
        
        logger.info(f"Deleted evaluation {evaluation_id} for material {material_id}")
        
        return Response(status_code=204)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting evaluation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete evaluation: {str(e)}"
        )
