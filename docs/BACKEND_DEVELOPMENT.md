# 🔧 Guía de Desarrollo del Backend - EduRAG

## 📋 Tabla de Contenidos

1. [Arquitectura del Backend](#arquitectura-del-backend)
2. [Configuración Inicial](#configuración-inicial)
3. [Estructura de Carpetas](#estructura-de-carpetas)
4. [Routers (API Layer)](#routers-api-layer)
5. [Services (Business Logic)](#services-business-logic)
6. [Core (Configuration)](#core-configuration)
7. [Dependencias](#dependencias)
8. [Patrones de Diseño](#patrones-de-diseño)
9. [Testing](#testing)
10. [Deployment](#deployment)

---

## 🏗️ Arquitectura del Backend

### Patrón: Arquitectura en Capas

```
┌───────────────────────────────────────┐
│         API Layer (Routers)           │  ← HTTP Handlers
│  - Validación de entrada              │
│  - Serialización de respuesta         │
│  - Manejo de errores HTTP             │
└───────────────┬───────────────────────┘
                │
┌───────────────▼───────────────────────┐
│      Service Layer (Services)         │  ← Business Logic
│  - Procesamiento de PDFs              │
│  - Interacción con OpenAI             │
│  - Lógica de negocio reutilizable     │
└───────────────┬───────────────────────┘
                │
┌───────────────▼───────────────────────┐
│     Data Access Layer (Core)          │  ← Database
│  - Cliente Supabase                   │
│  - Configuración de conexiones        │
│  - Queries a base de datos            │
└───────────────────────────────────────┘
```

### ¿Por Qué Esta Arquitectura?

**Ventajas:**

1. **Separación de Responsabilidades:**
   - Routers: Solo manejan HTTP
   - Services: Solo lógica de negocio
   - Core: Solo acceso a datos

2. **Testabilidad:**
   ```python
   # Fácil de testear con mocks
   def test_process_pdf():
       mock_db = Mock()
       service = PDFProcessor(db=mock_db)
       result = service.process("test.pdf")
       assert result.chunks_count == 10
   ```

3. **Reutilización:**
   ```python
   # Mismo servicio usado por múltiples routers
   # /api/materials/upload → pdf_processor.process()
   # /api/admin/reprocess/{id} → pdf_processor.process()
   ```

4. **Mantenibilidad:**
   - Cambiar DB no afecta services
   - Cambiar lógica no afecta routers
   - Agregar endpoints no duplica código

---

## ⚙️ Configuración Inicial

### 1. Entorno Virtual

```bash
# Crear entorno virtual
cd edurag/backend
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate
```

**¿Por qué venv?**
- Aísla dependencias del proyecto
- Evita conflictos entre proyectos
- Facilita deployment reproducible

### 2. Variables de Entorno

**Crear archivo `.env`:**

```env
# Supabase Configuration
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# OpenAI Configuration
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Application Configuration
ENV=development
DEBUG=True
LOG_LEVEL=DEBUG

# CORS Origins (comma separated)
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

**Cargar en Código:**

```python
# app/core/config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Supabase
    supabase_url: str
    supabase_key: str
    supabase_service_key: str | None = None
    
    # OpenAI
    openai_api_key: str
    
    # App
    env: str = "development"
    debug: bool = True
    log_level: str = "INFO"
    
    # CORS
    cors_origins: List[str] = ["http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

### 3. Instalación de Dependencias

```bash
pip install -r requirements.txt
```

**requirements.txt:**

```txt
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Database & Storage
supabase==2.0.3
postgrest==0.13.0

# AI & ML
openai==1.3.5
langchain==0.1.0
langchain-text-splitters==0.0.1

# PDF Processing
pdfplumber==0.11.7
PyPDF2==3.0.1

# Utilities
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Logging
python-json-logger==2.0.7
```

**Versiones Específicas:**
- Evitan breaking changes
- Reproducibilidad garantizada
- Facilitan debugging (misma versión en dev/prod)

---

## 📁 Estructura de Carpetas Detallada

```
backend/
├── app/
│   ├── __init__.py                    # Package initialization
│   │
│   ├── routers/                       # API Endpoints
│   │   ├── __init__.py
│   │   ├── auth.py                    # 🔐 Login, logout (preparado)
│   │   ├── students.py                # 👥 CRUD estudiantes
│   │   ├── courses.py                 # 📚 CRUD cursos
│   │   ├── materials.py               # 📄 Upload PDFs
│   │   ├── enrollments.py             # 📝 Inscripciones
│   │   ├── rag_vector.py              # 🤖 Chat RAG
│   │   └── analytics.py               # 📊 Estadísticas
│   │
│   ├── services/                      # Business Logic
│   │   ├── __init__.py
│   │   ├── pdf_processor.py           # 📄 Procesamiento PDFs
│   │   └── storage.py                 # 💾 Supabase Storage
│   │
│   ├── core/                          # Core Configuration
│   │   ├── __init__.py
│   │   ├── database.py                # 🗄️ Supabase client
│   │   ├── config.py                  # ⚙️ Settings (futuro)
│   │   └── security.py                # 🔒 Auth utilities (futuro)
│   │
│   └── models/                        # Pydantic Models (futuro)
│       ├── __init__.py
│       ├── student.py
│       ├── course.py
│       └── material.py
│
├── sql/                               # SQL Scripts
│   ├── create_tables.sql              # Schema inicial
│   └── create_vector_search_function.sql  # RPC function
│
├── logs/                              # Log files (git ignored)
│   └── app.log
│
├── tests/                             # Unit & Integration Tests
│   ├── __init__.py
│   ├── test_routers/
│   ├── test_services/
│   └── conftest.py                    # Pytest fixtures
│
├── main.py                            # 🚀 Application entry point
├── requirements.txt                   # Dependencies
├── .env                               # Environment variables (git ignored)
├── .env.example                       # Template de variables
├── .gitignore                         # Git ignore patterns
└── README.md                          # Backend-specific docs
```

---

## 🔌 Routers (API Layer)

### Anatomía de un Router

**Ejemplo: students.py**

```python
"""
Students Router - CRUD operations for students
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
import logging

from app.core.database import get_supabase_client

# ============================================================================
# LOGGING SETUP
# ============================================================================

logger = logging.getLogger(__name__)
router = APIRouter()


# ============================================================================
# PYDANTIC MODELS (Request/Response Schemas)
# ============================================================================

class StudentCreate(BaseModel):
    """Schema para crear estudiante"""
    name: str = Field(..., min_length=2, max_length=255, description="Nombre completo")
    email: EmailStr = Field(..., description="Email válido")
    cohort: str = Field(..., min_length=4, max_length=50, description="Cohorte (ej: 2024-A)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Juan Pérez",
                "email": "juan.perez@example.com",
                "cohort": "2024-A"
            }
        }


class StudentUpdate(BaseModel):
    """Schema para actualizar estudiante (campos opcionales)"""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    email: Optional[EmailStr] = None
    cohort: Optional[str] = Field(None, min_length=4, max_length=50)


class StudentResponse(BaseModel):
    """Schema de respuesta de estudiante"""
    id: str
    name: str
    email: str
    cohort: str
    created_at: str


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post(
    "/",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo estudiante",
    description="Crea un estudiante con nombre, email y cohorte",
    tags=["Students"]
)
async def create_student(student: StudentCreate):
    """
    Crea un nuevo estudiante en la base de datos.
    
    Args:
        student: Datos del estudiante (validados por Pydantic)
    
    Returns:
        dict: Mensaje de éxito y datos del estudiante creado
    
    Raises:
        HTTPException: 400 si hay error de validación
        HTTPException: 409 si el email ya existe
        HTTPException: 500 si hay error en el servidor
    """
    try:
        supabase = get_supabase_client()
        
        # Verificar si el email ya existe
        existing = supabase.table("students").select("id").eq("email", student.email).execute()
        if existing.data:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email {student.email} already exists"
            )
        
        # Insertar estudiante
        result = supabase.table("students").insert({
            "name": student.name,
            "email": student.email,
            "cohort": student.cohort
        }).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create student"
            )
        
        logger.info(f"Student created: {result.data[0]['id']} - {student.name}")
        
        return {
            "message": "Student created successfully",
            "data": result.data[0]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating student: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/",
    response_model=List[dict],
    summary="Listar todos los estudiantes",
    tags=["Students"]
)
async def get_students():
    """
    Obtiene lista de todos los estudiantes.
    
    Returns:
        List[dict]: Lista de estudiantes con todos sus campos
    """
    try:
        supabase = get_supabase_client()
        result = supabase.table("students").select("*").order("created_at", desc=True).execute()
        
        logger.debug(f"Retrieved {len(result.data or [])} students")
        
        return result.data or []
        
    except Exception as e:
        logger.error(f"Error fetching students: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/{student_id}",
    response_model=dict,
    summary="Obtener estudiante por ID",
    tags=["Students"]
)
async def get_student(student_id: str):
    """
    Obtiene un estudiante específico por su ID.
    
    Args:
        student_id: UUID del estudiante
    
    Returns:
        dict: Datos del estudiante
    
    Raises:
        HTTPException: 404 si no existe
    """
    try:
        supabase = get_supabase_client()
        result = supabase.table("students").select("*").eq("id", student_id).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with id {student_id} not found"
            )
        
        return result.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching student {student_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put(
    "/{student_id}",
    response_model=dict,
    summary="Actualizar estudiante",
    tags=["Students"]
)
async def update_student(student_id: str, student: StudentUpdate):
    """
    Actualiza campos de un estudiante.
    
    Args:
        student_id: UUID del estudiante
        student: Campos a actualizar (solo los presentes)
    
    Returns:
        dict: Mensaje de éxito y datos actualizados
    """
    try:
        supabase = get_supabase_client()
        
        # Construir objeto de actualización (solo campos presentes)
        update_data = student.model_dump(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        result = supabase.table("students").update(update_data).eq("id", student_id).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with id {student_id} not found"
            )
        
        logger.info(f"Student updated: {student_id}")
        
        return {
            "message": "Student updated successfully",
            "data": result.data[0]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating student {student_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete(
    "/{student_id}",
    response_model=dict,
    summary="Eliminar estudiante",
    tags=["Students"]
)
async def delete_student(student_id: str):
    """
    Elimina un estudiante y sus inscripciones (cascada).
    
    Args:
        student_id: UUID del estudiante
    
    Returns:
        dict: Mensaje de confirmación
    """
    try:
        supabase = get_supabase_client()
        
        # Eliminar inscripciones primero (evitar FK constraint)
        enrollments_result = supabase.table("enrollments").delete().eq("student_id", student_id).execute()
        deleted_enrollments = len(enrollments_result.data) if enrollments_result.data else 0
        
        # Eliminar estudiante
        result = supabase.table("students").delete().eq("id", student_id).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with id {student_id} not found"
            )
        
        logger.info(f"Student deleted: {student_id} (enrollments: {deleted_enrollments})")
        
        return {
            "message": f"Student deleted successfully. Enrollments deleted: {deleted_enrollments}",
            "deleted_enrollments": deleted_enrollments
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting student {student_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
```

### Patrones Importantes en Routers

#### 1. **Decoradores de FastAPI**

```python
@router.post(
    "/",                                    # Path
    response_model=dict,                    # Esquema de respuesta
    status_code=status.HTTP_201_CREATED,   # Código HTTP exitoso
    summary="Crear nuevo estudiante",       # Título en Swagger
    description="...",                      # Descripción detallada
    tags=["Students"]                       # Agrupación en Swagger
)
```

#### 2. **Validación Automática con Pydantic**

```python
class StudentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr  # Valida formato email automáticamente
    cohort: str = Field(..., min_length=4)
```

**Errores automáticos:**
- `name` faltante → 422 "field required"
- `name` con 1 carácter → 422 "string too short"
- `email` sin @ → 422 "invalid email format"

#### 3. **Manejo de Errores Consistente**

```python
try:
    # Código principal
    result = supabase.table("students").insert(data).execute()
    
    if not result.data:
        raise HTTPException(status_code=400, detail="Failed to create")
    
    return {"message": "Success", "data": result.data[0]}
    
except HTTPException:
    # Re-lanzar HTTPExceptions (ya tienen status code y detail)
    raise
    
except Exception as e:
    # Capturar errores inesperados
    logger.error(f"Unexpected error: {str(e)}", exc_info=True)
    raise HTTPException(status_code=500, detail=str(e))
```

#### 4. **Logging Estratégico**

```python
logger.info(f"Student created: {student_id}")      # Operaciones exitosas
logger.warning(f"Duplicate email: {email}")         # Situaciones inusuales
logger.error(f"DB error: {str(e)}", exc_info=True) # Errores (con traceback)
logger.debug(f"Query result: {result.data}")        # Debugging (verbose)
```

**Configuración de Logging:**

```python
# main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()  # También a consola
    ]
)
```

---

## 🛠️ Services (Business Logic)

### pdf_processor.py - Procesamiento de PDFs

**Responsabilidades:**
1. Extracción de texto desde PDFs
2. División en chunks con LangChain
3. Generación de embeddings con OpenAI
4. Almacenamiento en `material_chunks`

**Código Completo:**

```python
"""
PDF Processor Service - Extract, chunk, embed and store PDF content
"""

import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import OpenAI
import logging
from typing import List, Dict
from pathlib import Path

from app.core.database import get_supabase_client

logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

CHUNK_SIZE = 500        # Tokens por chunk
CHUNK_OVERLAP = 50      # Overlap entre chunks (preserva contexto)
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536


# ============================================================================
# PDF EXTRACTION
# ============================================================================

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extrae todo el texto de un archivo PDF.
    
    Args:
        file_path: Ruta al archivo PDF
    
    Returns:
        str: Texto completo del PDF
    
    Raises:
        Exception: Si el PDF está corrupto o no se puede leer
    """
    try:
        text_content = []
        
        with pdfplumber.open(file_path) as pdf:
            logger.info(f"Processing PDF: {Path(file_path).name} ({len(pdf.pages)} pages)")
            
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                
                if text:
                    text_content.append(text)
                    logger.debug(f"Page {i+1}: Extracted {len(text)} characters")
                else:
                    logger.warning(f"Page {i+1}: No text found")
        
        full_text = "\n\n".join(text_content)
        logger.info(f"Total text extracted: {len(full_text)} characters")
        
        return full_text
        
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise


# ============================================================================
# TEXT CHUNKING
# ============================================================================

def split_text_into_chunks(text: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> List[str]:
    """
    Divide texto en chunks usando LangChain RecursiveCharacterTextSplitter.
    
    Este splitter:
    - Intenta dividir por párrafos primero
    - Luego por oraciones
    - Luego por palabras
    - Finalmente por caracteres
    
    Esto preserva el contexto semántico mejor que división naive.
    
    Args:
        text: Texto completo a dividir
        chunk_size: Tamaño máximo de cada chunk en tokens
        chunk_overlap: Cantidad de tokens que se solapan entre chunks
    
    Returns:
        List[str]: Lista de chunks de texto
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]  # Orden de preferencia
        )
        
        chunks = text_splitter.split_text(text)
        
        logger.info(f"Text split into {len(chunks)} chunks (size: {chunk_size}, overlap: {chunk_overlap})")
        
        return chunks
        
    except Exception as e:
        logger.error(f"Error splitting text: {str(e)}")
        raise


# ============================================================================
# EMBEDDINGS GENERATION
# ============================================================================

def generate_embeddings(texts: List[str], openai_api_key: str) -> List[List[float]]:
    """
    Genera embeddings para una lista de textos usando OpenAI.
    
    Args:
        texts: Lista de textos (chunks)
        openai_api_key: API key de OpenAI
    
    Returns:
        List[List[float]]: Lista de vectores de embeddings (1536 dimensiones cada uno)
    
    Raises:
        Exception: Si la API de OpenAI falla
    """
    try:
        client = OpenAI(api_key=openai_api_key)
        embeddings = []
        
        # Procesar en lotes de 100 (límite de OpenAI por request)
        batch_size = 100
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            logger.debug(f"Generating embeddings for batch {i//batch_size + 1} ({len(batch)} chunks)")
            
            response = client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=batch,
                dimensions=EMBEDDING_DIMENSIONS
            )
            
            batch_embeddings = [item.embedding for item in response.data]
            embeddings.extend(batch_embeddings)
        
        logger.info(f"Generated {len(embeddings)} embeddings")
        
        return embeddings
        
    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")
        raise


# ============================================================================
# DATABASE STORAGE
# ============================================================================

def store_chunks_in_database(
    chunks: List[str],
    embeddings: List[List[float]],
    material_id: str,
    course_id: str
) -> int:
    """
    Almacena chunks y embeddings en la tabla material_chunks.
    
    Args:
        chunks: Lista de chunks de texto
        embeddings: Lista de vectores de embeddings
        material_id: UUID del material
        course_id: UUID del curso
    
    Returns:
        int: Número de chunks insertados
    
    Raises:
        Exception: Si falla la inserción en base de datos
    """
    try:
        supabase = get_supabase_client()
        
        # Preparar datos para inserción
        records = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            records.append({
                "material_id": material_id,
                "course_id": course_id,
                "chunk_index": i,
                "content": chunk,
                "embedding": embedding  # Lista de floats, Supabase convierte a vector
            })
        
        # Insertar en lotes de 100 (evitar timeouts)
        batch_size = 100
        total_inserted = 0
        
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            
            result = supabase.table("material_chunks").insert(batch).execute()
            
            if result.data:
                total_inserted += len(result.data)
                logger.debug(f"Inserted batch {i//batch_size + 1}: {len(result.data)} chunks")
        
        logger.info(f"Stored {total_inserted} chunks in database for material {material_id}")
        
        # Actualizar contador en tabla materials
        supabase.table("materials").update({
            "chunks_count": total_inserted,
            "processing_status": "completed"
        }).eq("id", material_id).execute()
        
        return total_inserted
        
    except Exception as e:
        logger.error(f"Error storing chunks in database: {str(e)}")
        
        # Marcar material como fallido
        try:
            supabase.table("materials").update({
                "processing_status": "failed"
            }).eq("id", material_id).execute()
        except:
            pass
        
        raise


# ============================================================================
# MAIN PROCESSING FUNCTION
# ============================================================================

async def process_pdf_material(
    file_path: str,
    material_id: str,
    course_id: str,
    openai_api_key: str
) -> Dict:
    """
    Pipeline completo de procesamiento de PDF:
    1. Extraer texto
    2. Dividir en chunks
    3. Generar embeddings
    4. Almacenar en DB
    
    Args:
        file_path: Ruta al archivo PDF
        material_id: UUID del material
        course_id: UUID del curso
        openai_api_key: API key de OpenAI
    
    Returns:
        dict: Resumen del procesamiento
    """
    try:
        logger.info(f"Starting PDF processing: {file_path}")
        
        # Actualizar estado a "processing"
        supabase = get_supabase_client()
        supabase.table("materials").update({
            "processing_status": "processing"
        }).eq("id", material_id).execute()
        
        # 1. Extraer texto
        text = extract_text_from_pdf(file_path)
        
        if not text or len(text.strip()) < 100:
            raise ValueError("PDF has insufficient text content")
        
        # 2. Dividir en chunks
        chunks = split_text_into_chunks(text)
        
        # 3. Generar embeddings
        embeddings = generate_embeddings(chunks, openai_api_key)
        
        # 4. Almacenar en DB
        chunks_count = store_chunks_in_database(chunks, embeddings, material_id, course_id)
        
        logger.info(f"PDF processing completed: {chunks_count} chunks created")
        
        return {
            "success": True,
            "chunks_count": chunks_count,
            "characters": len(text),
            "status": "completed"
        }
        
    except Exception as e:
        logger.error(f"PDF processing failed: {str(e)}", exc_info=True)
        
        # Marcar como fallido
        try:
            supabase = get_supabase_client()
            supabase.table("materials").update({
                "processing_status": "failed"
            }).eq("id", material_id).execute()
        except:
            pass
        
        return {
            "success": False,
            "error": str(e),
            "status": "failed"
        }
```

### Decisiones Técnicas en pdf_processor.py

#### ¿Por qué pdfplumber y no PyPDF2?

```python
# pdfplumber (mejor)
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
# - Maneja layouts complejos
# - Detecta tablas
# - Preserva espaciado

# PyPDF2 (limitado)
import PyPDF2
with open("file.pdf", "rb") as f:
    reader = PyPDF2.PdfReader(f)
    text = reader.pages[0].extract_text()
# - Falla con PDFs escaneados
# - Pierde formato de tablas
```

#### ¿Por qué RecursiveCharacterTextSplitter?

**Alternativas:**
- `CharacterTextSplitter`: División por caracteres (corta oraciones)
- `TokenTextSplitter`: División por tokens (más preciso pero más lento)
- `RecursiveCharacterTextSplitter`: **Mejor balance** (contexto + velocidad)

**Comportamiento:**
```python
text = """
Capítulo 1: Introducción

El cableado estructurado es...

Capítulo 2: Normas
"""

# RecursiveCharacterTextSplitter intenta:
# 1. Dividir por "\n\n" (párrafos) → Preserva capítulos completos
# 2. Si chunk > max_size, dividir por "\n" (líneas)
# 3. Si aún > max_size, dividir por ". " (oraciones)
# 4. Último recurso: dividir por caracteres

# Resultado: Chunks semánticamente coherentes
```

#### ¿Por qué chunk_overlap de 50?

Sin overlap:
```
Chunk 1: "...el cable Cat6 permite hasta 1Gbps."
Chunk 2: "El estándar TIA-568 define..."
# Si preguntan sobre "Cat6 y TIA-568", puede fallar
```

Con overlap de 50:
```
Chunk 1: "...el cable Cat6 permite hasta 1Gbps. El estándar TIA-568..."
Chunk 2: "El estándar TIA-568 define las normas de cableado..."
# Ambos chunks tienen contexto compartido
```

**Trade-off:**
- Más overlap = Mejor contexto = Mayor costo de storage
- 50 tokens (~10% de 500) es un balance óptimo

---

## 🗄️ Core (Configuration)

### database.py - Cliente Supabase

```python
"""
Database Core - Supabase client configuration
"""

from supabase import create_client, Client
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

# ============================================================================
# SINGLETON PATTERN
# ============================================================================

_supabase_client: Client | None = None


def get_supabase_client() -> Client:
    """
    Obtiene instancia singleton del cliente Supabase.
    
    Patrón Singleton:
    - Una sola instancia para toda la aplicación
    - Reutiliza conexiones (pool interno)
    - Evita múltiples autenticaciones
    
    Returns:
        Client: Instancia de cliente Supabase
    
    Raises:
        ValueError: Si faltan variables de entorno
    """
    global _supabase_client
    
    if _supabase_client is None:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError(
                "Missing Supabase credentials. "
                "Set SUPABASE_URL and SUPABASE_KEY in .env file"
            )
        
        _supabase_client = create_client(supabase_url, supabase_key)
        logger.info("Supabase client initialized")
    
    return _supabase_client


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def test_connection() -> bool:
    """
    Verifica que la conexión a Supabase funciona.
    
    Returns:
        bool: True si la conexión es exitosa
    """
    try:
        client = get_supabase_client()
        # Query simple para verificar conexión
        result = client.table("students").select("id").limit(1).execute()
        logger.info("Supabase connection test: SUCCESS")
        return True
    except Exception as e:
        logger.error(f"Supabase connection test: FAILED - {str(e)}")
        return False
```

### ¿Por qué Patrón Singleton?

**Sin Singleton:**
```python
# Cada request crea nueva conexión
def get_students():
    supabase = create_client(url, key)  # ❌ Nueva conexión
    return supabase.table("students").select("*").execute()

# Con 100 requests simultáneos:
# - 100 conexiones nuevas
# - 100 autenticaciones
# - Mayor latencia
# - Más uso de recursos
```

**Con Singleton:**
```python
# Todas las requests comparten una instancia
_client = None

def get_supabase_client():
    global _client
    if _client is None:
        _client = create_client(url, key)  # ✅ Solo una vez
    return _client

# Con 100 requests simultáneos:
# - 1 conexión (con pool interno)
# - 1 autenticación
# - Latencia mínima
# - Eficiente
```

---

## 📦 Dependencias Críticas

### FastAPI + Uvicorn

```bash
pip install fastapi==0.104.1 uvicorn[standard]==0.24.0
```

**¿Por qué `uvicorn[standard]`?**
- Incluye `uvloop` (event loop más rápido que asyncio)
- Incluye `httptools` (parser HTTP en C, más rápido)
- Incluye `websockets` (soporte WebSocket)

**Alternativas:**
- `gunicorn` con workers uvicorn (producción multi-core)
- `hypercorn` (ASGI server alternativo)

### Supabase Client

```bash
pip install supabase==2.0.3
```

**Funcionalidades usadas:**
```python
# CRUD con auto-parsing
result = supabase.table("students").select("*").execute()
data = result.data  # Lista de dicts

# Filters
supabase.table("students").select("*").eq("cohort", "2024-A").execute()
supabase.table("materials").select("*").neq("status", "failed").execute()
supabase.table("enrollments").select("*").in_("status", ["active", "completed"]).execute()

# Joins (Supabase auto-joins con foreign keys)
supabase.table("enrollments").select("*, students(*), courses(*)").execute()

# RPC (llamar funciones SQL)
supabase.rpc("match_material_chunks", {
    "query_embedding": vector,
    "match_threshold": 0.3
}).execute()

# Storage
supabase.storage.from_("course-materials").upload("path/file.pdf", file_bytes)
```

### OpenAI Client

```bash
pip install openai==1.3.5
```

**Uso:**
```python
from openai import OpenAI

client = OpenAI(api_key=api_key)

# Embeddings
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=["texto 1", "texto 2"],
    dimensions=1536
)
embeddings = [item.embedding for item in response.data]

# Chat Completion
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Eres un asistente educativo"},
        {"role": "user", "content": "Explica qué es RAG"}
    ],
    temperature=0.7,
    max_tokens=1000
)
answer = response.choices[0].message.content
```

### LangChain

```bash
pip install langchain==0.1.0 langchain-text-splitters==0.0.1
```

**Solo para chunking:**
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_text(long_text)
```

**Nota:** No usamos cadenas completas de LangChain (DocumentLoader, VectorStores, etc.) porque:
1. Tenemos control total sobre el pipeline
2. Evitamos abstracciones innecesarias
3. Mejor performance (menos overhead)
4. Más fácil de debuggear

---

## 🏁 Inicialización de la Aplicación

### main.py

```python
"""
EduRAG Backend - FastAPI Application
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

from app.routers import auth, students, courses, materials, enrollments, rag_vector, analytics
from app.core.database import test_connection

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# ============================================================================
# LIFESPAN EVENTS
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events - Ejecuta código al inicio y fin de la aplicación.
    """
    # Startup
    logger.info("=" * 60)
    logger.info("EduRAG Backend Starting...")
    logger.info("=" * 60)
    
    # Verificar conexión a Supabase
    if test_connection():
        logger.info("✓ Supabase connection successful")
    else:
        logger.error("✗ Supabase connection failed")
    
    logger.info("Server ready to accept requests")
    
    yield  # Aplicación corriendo
    
    # Shutdown
    logger.info("EduRAG Backend Shutting down...")


# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="EduRAG API",
    description="Sistema de gestión educativa con RAG inteligente",
    version="1.0.0",
    docs_url="/docs",        # Swagger UI
    redoc_url="/redoc",      # ReDoc
    lifespan=lifespan
)


# ============================================================================
# CORS MIDDLEWARE
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",    # Vite dev server
        "http://127.0.0.1:5173",
        "http://localhost:3000",    # Alternativo
    ],
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Content-Type, Authorization, etc.
)


# ============================================================================
# ROUTERS
# ============================================================================

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(students.router, prefix="/api/students", tags=["Students"])
app.include_router(courses.router, prefix="/api/courses", tags=["Courses"])
app.include_router(materials.router, prefix="/api/materials", tags=["Materials"])
app.include_router(enrollments.router, prefix="/api/enrollments", tags=["Enrollments"])
app.include_router(rag_vector.router, prefix="/api/rag", tags=["RAG"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Health check endpoint"""
    return {
        "name": "EduRAG API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",      # Escuchar en todas las interfaces
        port=8000,
        reload=True,          # Auto-reload en desarrollo
        log_level="info"
    )
```

### Iniciar Servidor

```bash
# Opción 1: Desde main.py
python main.py

# Opción 2: Con uvicorn directamente
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Opción 3: Con configuración custom
uvicorn main:app --reload --log-config logging.conf
```

---

## 🔗 Próximo Documento

Continúa con [FRONTEND_DEVELOPMENT.md](FRONTEND_DEVELOPMENT.md) para entender la arquitectura del frontend Vue 3.

---

*Última actualización: Octubre 23, 2025*
*Versión: 1.0.0*
