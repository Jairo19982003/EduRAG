"""
Materials Router - Manage course materials with PDF upload support
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import logging
import tempfile
import os
import uuid

from app.core.database import get_supabase_client
from app.services.pdf_processor import process_pdf_file, delete_material_chunks
from app.services.storage import upload_pdf_to_storage, delete_pdf_from_storage

logger = logging.getLogger(__name__)
router = APIRouter()


class MaterialCreate(BaseModel):
    """Material creation model"""
    title: str
    course_id: str  # UUID as string
    mime_type: str = "application/pdf"
    author: Optional[str] = None
    file_url: Optional[str] = None
    raw_text: Optional[str] = None


async def process_pdf_background(file_path: str, material_id: str, storage_path: str):
    """Background task to process PDF after upload"""
    try:
        logger.info(f"Starting background PDF processing for material {material_id}")
        
        # Process PDF: extract, chunk, embed, store
        result = await process_pdf_file(file_path, material_id)
        
        logger.info(f"PDF processing completed: {result['chunks_created']} chunks created")
        
        # Update material with storage path
        supabase = get_supabase_client()
        supabase.table("materials").update({
            "file_url": storage_path
        }).eq("id", material_id).execute()
        
    except Exception as e:
        logger.error(f"Background PDF processing failed: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)


@router.post("/upload-pdf", response_model=dict)
async def upload_pdf_material(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: str = Form(...),
    course_id: str = Form(...),
    author: Optional[str] = Form(None)
):
    """
    Upload a PDF material and process it automatically
    
    Steps:
    1. Validate PDF file
    2. Create material record
    3. Upload PDF to Supabase Storage
    4. Extract text from PDF
    5. Chunk text (500 tokens, 50 overlap)
    6. Generate embeddings
    7. Store chunks in database
    
    Processing happens in background, returns immediately
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        if not file.content_type == 'application/pdf':
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        # Read file content
        file_content = await file.read()
        
        # Validate file size (max 50MB)
        max_size = 50 * 1024 * 1024  # 50MB in bytes
        if len(file_content) > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size is 50MB, got {len(file_content) / 1024 / 1024:.2f}MB"
            )
        
        if len(file_content) == 0:
            raise HTTPException(status_code=400, detail="Empty file")
        
        # Create material record
        supabase = get_supabase_client()
        material_id = str(uuid.uuid4())
        
        material_data = {
            "id": material_id,
            "title": title,
            "course_id": course_id,
            "mime_type": "application/pdf",
            "author": author,
            "processing_status": "pending",
            "chunks_count": 0
        }
        
        result = supabase.table("materials").insert(material_data).execute()
        
        if not result.data:
            raise HTTPException(status_code=400, detail="Failed to create material record")
        
        # Upload to Supabase Storage
        storage_path = await upload_pdf_to_storage(file_content, file.filename, material_id)
        
        # Save to temporary file for processing
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_file.write(file_content)
        temp_file.close()
        
        # Schedule background processing
        background_tasks.add_task(
            process_pdf_background,
            temp_file.name,
            material_id,
            storage_path
        )
        
        logger.info(f"PDF uploaded successfully: {title} (material_id: {material_id})")
        
        return {
            "message": "PDF uploaded successfully. Processing in background...",
            "material_id": material_id,
            "title": title,
            "file_size_mb": round(len(file_content) / 1024 / 1024, 2),
            "status": "processing"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.post("/", response_model=dict)
async def create_material(material: MaterialCreate):
    """Create a new material (manual text entry - legacy)"""
    try:
        supabase = get_supabase_client()
        result = supabase.table("materials").insert(material.dict()).execute()
        
        if result.data:
            logger.info(f"Material created: {material.title}")
            return {"message": "Material created successfully", "data": result.data[0]}
        else:
            raise HTTPException(status_code=400, detail="Failed to create material")
    except Exception as e:
        logger.error(f"Error creating material: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[dict])
async def get_materials():
    """Get all materials"""
    try:
        supabase = get_supabase_client()
        result = supabase.table("materials").select("*").execute()
        return result.data if result.data else []
    except Exception as e:
        logger.error(f"Error fetching materials: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{material_id}", response_model=dict)
async def get_material(material_id: str):
    """Get a specific material with processing status"""
    try:
        supabase = get_supabase_client()
        result = supabase.table("materials").select("*").eq("id", material_id).execute()
        
        if result.data:
            return result.data[0]
        else:
            raise HTTPException(status_code=404, detail="Material not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching material: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{material_id}", response_model=dict)
async def delete_material(material_id: str):
    """Delete a material and all its chunks"""
    try:
        supabase = get_supabase_client()
        
        # Get material to find storage path
        material_result = supabase.table("materials").select("*").eq("id", material_id).execute()
        
        if not material_result.data:
            raise HTTPException(status_code=404, detail="Material not found")
        
        material = material_result.data[0]
        
        # Delete chunks (CASCADE should handle this, but being explicit)
        try:
            await delete_material_chunks(material_id)
        except Exception as e:
            logger.warning(f"Error deleting chunks: {e}")
        
        # Delete from storage if exists
        if material.get("file_url"):
            try:
                await delete_pdf_from_storage(material["file_url"])
            except Exception as e:
                logger.warning(f"Error deleting from storage: {e}")
        
        # Delete material record
        supabase.table("materials").delete().eq("id", material_id).execute()
        
        logger.info(f"Material deleted: {material_id}")
        return {"message": "Material deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting material: {e}")
        raise HTTPException(status_code=500, detail=str(e))
