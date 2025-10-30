"""
RAG Router - Retrieval Augmented Generation
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..core.database import get_supabase_client
from ..core.config import Settings
import logging
import openai

router = APIRouter()
logger = logging.getLogger(__name__)
settings = Settings()

# Configure OpenAI
openai.api_key = settings.OPENAI_API_KEY


class QueryRequest(BaseModel):
    """Query request model"""
    question: str
    course_id: Optional[str] = None
    material_id: Optional[str] = None


@router.post("/query", response_model=dict)
async def query_materials(request: QueryRequest):
    """Query materials using RAG with OpenAI"""
    try:
        supabase = get_supabase_client()
        
        # Build query based on filters
        query = supabase.table("materials").select("*, courses(code, name)")
        
        if request.material_id:
            query = query.eq("id", request.material_id)
            logger.info(f"Filtering by material_id: {request.material_id}")
        elif request.course_id:
            query = query.eq("course_id", request.course_id)
            logger.info(f"Filtering by course_id: {request.course_id}")
        else:
            logger.info("Querying all materials")
        
        result = query.execute()
        materials = result.data or []
        
        logger.info(f"Found {len(materials)} materials")
        
        if not materials:
            return {
                "answer": "❌ No encontré materiales con los filtros seleccionados.\n\n💡 Consejo: Verifica que haya materiales en ese curso o intenta con 'Todos los cursos'.",
                "sources": [],
                "context": "Sin materiales disponibles"
            }
        
        # Extract text from materials
        all_text = []
        sources = []
        
        for material in materials:
            text = material.get('raw_text', '').strip()
            course = material.get('courses', {})
            
            sources.append({
                'title': material.get('title', 'Sin título'),
                'course': f"{course.get('code', '')} - {course.get('name', '')}",
                'author': material.get('author', 'Desconocido')
            })
            
            if text:
                all_text.append(text)
                logger.info(f"Material '{material.get('title')}' has {len(text)} characters")
            else:
                logger.warning(f"Material '{material.get('title')}' has NO TEXT in raw_text field")
        
        if not all_text:
            material_names = [m.get('title') for m in materials]
            return {
                "answer": f"⚠️ **Encontré {len(materials)} material(es), pero ninguno tiene contenido de texto.**\n\n📝 Materiales encontrados:\n" + "\n".join(f"• {name}" for name in material_names) + "\n\n💡 **Solución:** Ve a Administración → Materiales y agrega contenido en el campo 'Contenido/Texto' al crear o editar el material.",
                "sources": sources,
                "context": f"{len(materials)} materiales sin texto procesable"
            }
        
        # Combine all text for context
        combined_text = "\n\n".join(all_text)
        logger.info(f"Total text length: {len(combined_text)} characters")
        
        # === NUEVA IMPLEMENTACIÓN: Usar OpenAI para RAG ===
        try:
            # Truncate context if too long (OpenAI has token limits)
            max_context_length = 8000  # Leave room for question and response
            if len(combined_text) > max_context_length:
                combined_text = combined_text[:max_context_length] + "\n\n[...contenido truncado por límite de tokens...]"
                logger.info(f"Context truncated to {max_context_length} characters")
            
            # Build system prompt
            system_prompt = f"""Eres un asistente educativo experto que ayuda a estudiantes a entender materiales de cursos.

Tu tarea es responder preguntas basándote ÚNICAMENTE en el contexto proporcionado de los materiales del curso.

Instrucciones:
1. Responde en español de forma clara y educativa
2. Si la información está en el contexto, proporciona una respuesta detallada
3. Si NO está en el contexto, di claramente que no encontraste esa información
4. Cita fragmentos relevantes del material cuando sea apropiado
5. Sé conciso pero completo

CONTEXTO DE LOS MATERIALES:
{combined_text}
"""
            
            # Call OpenAI API
            logger.info(f"Calling OpenAI API with model: {settings.OPENAI_MODEL}")
            
            response = openai.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": request.question}
                ],
                temperature=0.7,
                max_tokens=800,
                top_p=0.9
            )
            
            ai_answer = response.choices[0].message.content
            logger.info(f"OpenAI response received: {len(ai_answer)} characters")
            
            return {
                "answer": ai_answer,
                "sources": sources,
                "context": f"✨ Respuesta generada por IA • Consultados {len(materials)} materiales • {len(combined_text)} caracteres de contexto"
            }
            
        except openai.OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            # Fallback to keyword search if OpenAI fails
            return await fallback_keyword_search(request.question, combined_text, sources, len(materials))
        
    except Exception as e:
        logger.error(f"Error processing RAG query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error al procesar la consulta: {str(e)}")


async def fallback_keyword_search(question: str, combined_text: str, sources: list, material_count: int):
    """Fallback search method when OpenAI is unavailable"""
    logger.info("Using fallback keyword search")
    
    question_lower = question.lower()
    combined_text_lower = combined_text.lower()
    
    # Extract keywords
    stop_words = {'que', 'es', 'el', 'la', 'los', 'las', 'un', 'una', 'de', 'del', 'en', 'por', 'para', 'con', 'sobre', 'como', 'qué', 'cuál', 'cómo'}
    keywords = [kw for kw in question_lower.split() if len(kw) > 2 and kw not in stop_words]
    relevant_keywords = [kw for kw in keywords if kw in combined_text_lower]
    
    if not relevant_keywords:
        answer = f"🤔 **No encontré coincidencias exactas para tu pregunta.**\n\n"
        answer += f"📚 **Vista previa del material:**\n{combined_text[:300]}...\n\n"
        answer += "💡 **Nota:** Servicio de IA temporalmente no disponible. Usa búsqueda por palabras clave."
    else:
        sentences = []
        for sep in ['. ', '.\n', '! ', '? ']:
            if sep in combined_text:
                sentences = combined_text.split(sep)
                break
        
        if not sentences:
            sentences = [combined_text]
        
        relevant_sentences = []
        for sentence in sentences:
            if any(kw in sentence.lower() for kw in relevant_keywords):
                relevant_sentences.append(sentence.strip())
                if len(relevant_sentences) >= 3:
                    break
        
        if relevant_sentences:
            answer = "✅ **Información encontrada:**\n\n"
            answer += ". ".join(relevant_sentences[:2]) + "."
            answer += f"\n\n🔑 **Palabras clave:** {', '.join(relevant_keywords)}"
        else:
            answer = f"El material contiene información relacionada.\n\n"
            answer += f"📄 **Fragmento:**\n{combined_text[:300]}..."
    
    return {
        "answer": answer + "\n\n⚠️ _Respuesta generada por búsqueda básica (OpenAI no disponible)_",
        "sources": sources,
        "context": f"Búsqueda por keywords • {material_count} materiales consultados"
    }


@router.post("/chat", response_model=dict)
async def chat(request: QueryRequest):
    """Legacy chat endpoint - redirects to query"""
    return await query_materials(request)
