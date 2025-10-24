"""
RAG Router - Retrieval Augmented Generation with Vector Search
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from openai import AsyncOpenAI
import logging

from app.core.database import get_supabase_client
from app.core.config import settings
from app.services.pdf_processor import generate_embeddings

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize OpenAI client
openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


class QueryRequest(BaseModel):
    """Query request model"""
    question: str
    course_id: Optional[str] = None
    material_id: Optional[str] = None
    top_k: int = 5  # Number of chunks to retrieve


async def get_relevant_chunks(
    question: str,
    course_id: Optional[str] = None,
    material_id: Optional[str] = None,
    top_k: int = 5
) -> List[dict]:
    """
    Retrieve most relevant chunks using vector similarity search
    
    Args:
        question: User's question
        course_id: Optional course filter
        material_id: Optional material filter
        top_k: Number of chunks to retrieve
        
    Returns:
        List of relevant chunk dictionaries
    """
    try:
        supabase = get_supabase_client()
        
        # Generate embedding for the question
        question_embeddings = await generate_embeddings([question])
        question_embedding = question_embeddings[0]
        
        # Build the query with filters
        # Use the view that includes course and material metadata
        # Lower threshold to 0.3 for better results
        query = supabase.rpc(
            'match_material_chunks',
            {
                'query_embedding': question_embedding,
                'match_threshold': 0.3,  # Lowered from 0.7 to get more results
                'match_count': top_k,
                'filter_course_id': course_id,
                'filter_material_id': material_id
            }
        )
        
        result = query.execute()
        
        logger.info(f"RPC response status: {result.count if hasattr(result, 'count') else 'N/A'}")
        logger.info(f"Chunks returned: {len(result.data) if result.data else 0}")
        if result.data and len(result.data) > 0:
            logger.info(f"First chunk similarity: {result.data[0].get('similarity', 'N/A')}")
        
        return result.data if result.data else []
        
    except Exception as e:
        logger.error(f"Error retrieving chunks: {str(e)}")
        # Fallback to basic search if vector search fails
        return []


async def generate_answer_with_context(
    question: str,
    chunks: List[dict]
) -> str:
    """
    Generate answer using OpenAI with retrieved context chunks
    
    Args:
        question: User's question
        chunks: Retrieved context chunks
        
    Returns:
        Generated answer
    """
    try:
        if not chunks:
            return (
                "❌ No encontré información relevante para responder tu pregunta.\n\n"
                "💡 Consejos:\n"
                "• Verifica que hay materiales subidos en el curso seleccionado\n"
                "• Intenta reformular tu pregunta de manera más específica\n"
                "• Asegúrate de que los PDFs contienen información sobre el tema"
            )
        
        # Build context from chunks
        context_parts = []
        sources = []
        
        for i, chunk in enumerate(chunks, 1):
            context_parts.append(
                f"[Fragmento {i}]\n"
                f"Fuente: {chunk.get('material_title', 'Desconocido')}\n"
                f"Curso: {chunk.get('course_code', '')} - {chunk.get('course_name', '')}\n"
                f"Página: {chunk.get('metadata', {}).get('page', 'N/A')}\n"
                f"Contenido:\n{chunk.get('chunk_text', '')}\n"
            )
            
            # Track unique sources
            source_key = chunk.get('material_id')
            if source_key and not any(s['id'] == source_key for s in sources):
                sources.append({
                    'id': source_key,
                    'title': chunk.get('material_title', 'Sin título'),
                    'course': f"{chunk.get('course_code', '')} - {chunk.get('course_name', '')}",
                    'author': chunk.get('author', 'Desconocido')
                })
        
        context = "\n\n".join(context_parts)
        
        # System prompt
        system_prompt = f"""Eres un asistente educativo inteligente especializado en responder preguntas sobre materiales académicos.

Tu trabajo es:
1. Analizar cuidadosamente los fragmentos de texto proporcionados
2. Responder la pregunta del usuario de manera precisa y completa
3. Basar tu respuesta SOLO en la información de los fragmentos
4. Si la información está en varios fragmentos, sintetizar una respuesta coherente
5. Citar las fuentes cuando sea posible (mencionar de qué material proviene la información)
6. Usar formato Markdown para mejor legibilidad

Reglas importantes:
- NO inventes información que no esté en los fragmentos
- Si los fragmentos no contienen suficiente información, indícalo claramente
- Sé conciso pero completo
- Usa ejemplos de los fragmentos cuando sea apropiado
- Estructura tu respuesta con títulos, listas o puntos cuando ayude a la claridad

Fragmentos de contexto:
{context}

Fuentes disponibles:
{chr(10).join([f"• {s['title']} ({s['course']})" for s in sources])}
"""
        
        # Generate answer with OpenAI
        response = await openai_client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.3,  # Lower temperature for more focused answers
            max_tokens=1000
        )
        
        answer = response.choices[0].message.content
        
        # Add sources at the end
        answer += "\n\n---\n\n**📚 Fuentes consultadas:**\n"
        for source in sources:
            answer += f"- {source['title']} ({source['course']})\n"
        
        return answer
        
    except Exception as e:
        logger.error(f"Error generating answer: {str(e)}")
        return f"❌ Error al generar respuesta: {str(e)}"


@router.post("/query", response_model=dict)
async def query_materials(request: QueryRequest):
    """
    Query materials using vector similarity search + OpenAI
    
    Process:
    1. Generate embedding for user question
    2. Retrieve most similar chunks from database (pgvector)
    3. Use OpenAI to generate answer based on retrieved chunks
    4. Return answer with sources
    """
    try:
        logger.info(f"RAG query: '{request.question[:50]}...'")
        
        if request.material_id:
            logger.info(f"Filtering by material_id: {request.material_id}")
        elif request.course_id:
            logger.info(f"Filtering by course_id: {request.course_id}")
        
        # Retrieve relevant chunks using vector search
        chunks = await get_relevant_chunks(
            question=request.question,
            course_id=request.course_id,
            material_id=request.material_id,
            top_k=request.top_k
        )
        
        logger.info(f"Retrieved {len(chunks)} relevant chunks")
        
        # Generate answer with context
        answer = await generate_answer_with_context(request.question, chunks)
        
        # Extract sources
        sources = []
        seen_materials = set()
        
        for chunk in chunks:
            material_id = chunk.get('material_id')
            if material_id and material_id not in seen_materials:
                seen_materials.add(material_id)
                sources.append({
                    'title': chunk.get('material_title', 'Sin título'),
                    'course': f"{chunk.get('course_code', '')} - {chunk.get('course_name', '')}",
                    'author': chunk.get('author', 'Desconocido'),
                    'page': chunk.get('metadata', {}).get('page', 'N/A')
                })
        
        return {
            "answer": answer,
            "sources": sources,
            "chunks_used": len(chunks),
            "model": settings.OPENAI_MODEL
        }
        
    except Exception as e:
        logger.error(f"RAG query error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@router.get("/health", response_model=dict)
async def health_check():
    """Check RAG system health"""
    try:
        supabase = get_supabase_client()
        
        # Check if material_chunks table exists and has data
        result = supabase.table("material_chunks").select("id, material_id, chunk_index, embedding").limit(5).execute()
        has_chunks = len(result.data) > 0 if result.data else False
        
        chunks_info = []
        if result.data:
            for chunk in result.data:
                chunks_info.append({
                    "id": chunk.get("id"),
                    "material_id": chunk.get("material_id"),
                    "chunk_index": chunk.get("chunk_index"),
                    "has_embedding": chunk.get("embedding") is not None,
                    "embedding_length": len(chunk.get("embedding", [])) if chunk.get("embedding") else 0
                })
        
        # Check materials count
        materials = supabase.table("materials").select("id, processing_status, chunks_count").execute()
        total_materials = len(materials.data) if materials.data else 0
        
        processed_materials = sum(
            1 for m in (materials.data or [])
            if m.get('processing_status') == 'completed'
        )
        
        # Count total chunks
        chunk_count_result = supabase.table("material_chunks").select("id", count="exact").execute()
        total_chunks = chunk_count_result.count if hasattr(chunk_count_result, 'count') else 0
        
        return {
            "status": "healthy",
            "vector_search": "enabled",
            "has_chunks": has_chunks,
            "total_chunks": total_chunks,
            "total_materials": total_materials,
            "processed_materials": processed_materials,
            "sample_chunks": chunks_info,
            "openai_model": settings.OPENAI_MODEL,
            "embedding_model": settings.OPENAI_EMBEDDING_MODEL
        }
        
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }
