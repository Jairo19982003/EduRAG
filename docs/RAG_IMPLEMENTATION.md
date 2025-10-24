# 🤖 Implementación del Sistema RAG - EduRAG

## 📋 Contenido

1. [¿Qué es RAG?](#qué-es-rag)
2. [Pipeline Completo](#pipeline-completo)
3. [Procesamiento de PDFs](#procesamiento-de-pdfs)
4. [Generación de Embeddings](#generación-de-embeddings)
5. [Búsqueda Vectorial](#búsqueda-vectorial)
6. [Generación de Respuestas](#generación-de-respuestas)
7. [Optimizaciones](#optimizaciones)

---

## 🎯 ¿Qué es RAG?

**RAG (Retrieval-Augmented Generation)** es un patrón arquitectónico que combina:

1. **Retrieval (Recuperación):** Búsqueda de información relevante en una base de conocimiento
2. **Augmented (Aumentado):** Agregar esa información al contexto del LLM
3. **Generation (Generación):** LLM genera respuesta basada en el contexto

### RAG vs LLM Puro

**LLM Puro (sin RAG):**

```python
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "¿Qué es el cableado estructurado?"}
    ]
)
# Respuesta basada en conocimiento pre-entrenado (hasta Sep 2023)
# ❌ No sabe sobre materiales específicos del curso
# ❌ Puede "alucinar" información incorrecta
# ❌ No cita fuentes verificables
```

**Con RAG:**

```python
# 1. Buscar información relevante
chunks = search_in_database("¿Qué es el cableado estructurado?")

# 2. Construir contexto
context = "\n\n".join([chunk.content for chunk in chunks])

# 3. Generar respuesta con contexto
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": f"Responde basándote en este contexto:\n{context}"},
        {"role": "user", "content": "¿Qué es el cableado estructurado?"}
    ]
)
# ✅ Respuesta basada en materiales específicos del curso
# ✅ Información actualizada y verificable
# ✅ Cita fuentes con títulos y autores
```

### Ventajas de RAG

| Aspecto | LLM Puro | RAG |
|---------|----------|-----|
| Conocimiento | Hasta fecha de entrenamiento | Actualizable en tiempo real |
| Precisión | Puede alucinar | Basado en fuentes reales |
| Fuentes | No cita | Cita documentos específicos |
| Dominio específico | Genérico | Especializado en materiales del curso |
| Costo | $0.15 por 1M tokens | $0.17 por 1M tokens (embedding + chat) |

---

## 🔄 Pipeline Completo

### Diagrama de Flujo

```
┌─────────────────────────────────────────────────────────────┐
│                    FASE 1: INDEXACIÓN                        │
│                  (Una vez por material)                      │
└─────────────────────────────────────────────────────────────┘

    Usuario sube PDF
         │
         ▼
    ┌──────────────┐
    │ Upload PDF   │  ← Supabase Storage
    │ to Storage   │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ Extract Text │  ← pdfplumber
    │ from PDF     │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ Split into   │  ← LangChain RecursiveTextSplitter
    │ Chunks       │     (500 tokens, 50 overlap)
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ Generate     │  ← OpenAI text-embedding-3-small
    │ Embeddings   │     (1536 dimensions)
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ Store in DB  │  ← PostgreSQL + pgvector
    │ with Vectors │     HNSW index
    └──────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    FASE 2: CONSULTA                          │
│                  (Cada vez que el usuario pregunta)          │
└─────────────────────────────────────────────────────────────┘

    Usuario hace pregunta
         │
         ▼
    ┌──────────────┐
    │ Convert      │  ← OpenAI text-embedding-3-small
    │ Query to     │     (mismo modelo que indexación)
    │ Embedding    │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ Vector       │  ← match_material_chunks() SQL
    │ Similarity   │     Cosine similarity > 0.3
    │ Search       │     Top 5 chunks
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ Build        │  ← Chunks + metadata
    │ Context      │     (course, material, author)
    │ Prompt       │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ Generate     │  ← OpenAI GPT-4o-mini
    │ Answer with  │     Temperature 0.7
    │ GPT-4        │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ Return       │  ← Answer + sources + similarities
    │ to User      │
    └──────────────┘
```

---

## 📄 Procesamiento de PDFs

### 1. Extracción de Texto

**Código (pdf_processor.py):**

```python
import pdfplumber

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extrae texto completo de un PDF.
    
    pdfplumber es superior a PyPDF2 porque:
    - Detecta layouts complejos (tablas, columnas)
    - Preserva formato y espaciado
    - Funciona con PDFs escaneados (con OCR adicional)
    """
    text_content = []
    
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)
    
    return "\n\n".join(text_content)
```

**Ejemplo de Salida:**

```
CAPÍTULO 1: CABLEADO ESTRUCTURADO

1.1 Introducción

El cableado estructurado es un sistema de cables, conectores...

1.2 Normas y Estándares

Las principales normas que regulan el cableado estructurado son:
- ANSI/TIA-568: Estándar de cableado comercial
- ISO/IEC 11801: Estándar internacional...
```

### 2. Chunking Inteligente

**¿Por qué necesitamos chunks?**

- **Limitación de contexto:** GPT-4o-mini tiene ventana de 128K tokens (~96K palabras)
- **Precisión:** Chunks pequeños = búsquedas más precisas
- **Performance:** Procesar 1000 chunks es más rápido que 1 documento gigante

**Código (pdf_processor.py):**

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text_into_chunks(text: str) -> List[str]:
    """
    Divide texto usando estrategia recursiva.
    
    Estrategia de división (en orden de prioridad):
    1. Párrafos (\n\n) - Preserva contexto semántico completo
    2. Líneas (\n) - Si párrafo es muy largo
    3. Oraciones (. ) - Si línea es muy larga
    4. Palabras ( ) - Si oración es muy larga
    5. Caracteres - Último recurso
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,        # Tamaño objetivo en caracteres
        chunk_overlap=50,      # Solapamiento entre chunks
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = splitter.split_text(text)
    return chunks
```

**Ejemplo de Chunks:**

```python
text = """
CAPÍTULO 1: INTRODUCCIÓN

El cableado estructurado es fundamental...

CAPÍTULO 2: NORMAS

Las normas principales son ANSI/TIA-568...
"""

chunks = split_text_into_chunks(text)

# Chunk 0:
"CAPÍTULO 1: INTRODUCCIÓN\n\nEl cableado estructurado es fundamental..."

# Chunk 1 (con overlap de 50 caracteres):
"...es fundamental para redes modernas.\n\nCAPÍTULO 2: NORMAS\n\nLas normas..."
```

### ¿Por qué chunk_size=500 y overlap=50?

**Tamaño de Chunk:**

```python
# Muy pequeño (100 caracteres)
❌ "El cableado estructurado es un sistema de cables"
# Falta contexto (¿qué tipo de sistema? ¿para qué?)

# Muy grande (2000 caracteres)
❌ Incluye múltiples conceptos diferentes
# Búsqueda menos precisa (trae información irrelevante)

# Óptimo (500 caracteres)
✅ "El cableado estructurado es un sistema de cables, conectores y 
   dispositivos que proporciona una infraestructura de telecomunicaciones
   flexible para edificios. Está regulado por normas ANSI/TIA-568 e 
   ISO/IEC 11801..."
# Contexto completo + enfocado
```

**Overlap:**

```python
# Sin overlap
Chunk 1: "...hasta 10 Gbps."
Chunk 2: "La norma TIA-568..."
# Si buscan "velocidad de TIA-568", no encuentra relación

# Con overlap de 50
Chunk 1: "...hasta 10 Gbps. La norma TIA-568..."
Chunk 2: "La norma TIA-568 especifica..."
# Ambos chunks tienen contexto compartido
```

---

## 🧠 Generación de Embeddings

### ¿Qué son los Embeddings?

**Embeddings** son representaciones numéricas (vectores) de texto que capturan significado semántico.

**Ejemplo Conceptual:**

```python
# Textos similares → vectores cercanos
embedding("gato") = [0.2, 0.8, 0.1, ...]      ─┐
embedding("felino") = [0.3, 0.7, 0.2, ...]    ─┤ Cercanos
embedding("cachorro") = [0.25, 0.75, 0.15, ...] ┘

embedding("computadora") = [0.9, 0.1, 0.8, ...] ← Lejano
```

### OpenAI text-embedding-3-small

**Especificaciones:**

- **Dimensiones:** 1536 (configurables: 512 a 3072)
- **Modelo:** Basado en transformer
- **Costo:** $0.02 por 1M tokens (~700K palabras)
- **Performance:** 62.3% en MTEB benchmark

**Código (pdf_processor.py):**

```python
from openai import OpenAI

def generate_embeddings(texts: List[str], api_key: str) -> List[List[float]]:
    """
    Genera embeddings para lista de textos.
    
    Args:
        texts: Chunks de texto
        api_key: OpenAI API key
    
    Returns:
        Lista de vectores [1536 dimensiones cada uno]
    """
    client = OpenAI(api_key=api_key)
    embeddings = []
    
    # Procesar en lotes de 100 (límite de OpenAI)
    batch_size = 100
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=batch,
            dimensions=1536
        )
        
        batch_embeddings = [item.embedding for item in response.data]
        embeddings.extend(batch_embeddings)
    
    return embeddings
```

**Resultado:**

```python
chunk = "El cableado estructurado es un sistema..."

embedding = generate_embeddings([chunk], api_key)[0]

print(len(embedding))  # 1536
print(embedding[:5])   # [0.0234, -0.0145, 0.0456, -0.0089, 0.0123]
```

### Almacenamiento en PostgreSQL

```python
def store_chunks_in_database(chunks, embeddings, material_id, course_id):
    """
    Inserta chunks con embeddings en material_chunks.
    """
    supabase = get_supabase_client()
    
    records = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        records.append({
            "material_id": material_id,
            "course_id": course_id,
            "chunk_index": i,
            "content": chunk,
            "embedding": embedding  # pgvector convierte lista a VECTOR
        })
    
    # Insertar en lotes
    batch_size = 100
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        supabase.table("material_chunks").insert(batch).execute()
```

---

## 🔍 Búsqueda Vectorial

### Similitud de Coseno

**Fórmula:**

```
cosine_similarity(A, B) = (A · B) / (||A|| * ||B||)

Donde:
- A · B = producto punto (sum(a_i * b_i))
- ||A|| = magnitud del vector A (sqrt(sum(a_i²)))
```

**Rango:** [-1, 1]
- 1 = Vectores idénticos (mismo significado)
- 0 = Vectores ortogonales (sin relación)
- -1 = Vectores opuestos

**PostgreSQL con pgvector:**

```sql
-- Operador <=> retorna distancia de coseno (0 a 2)
-- Convertimos a similitud: 1 - distancia
SELECT
    content,
    (1 - (embedding <=> query_vector)) AS similarity
FROM material_chunks
WHERE (1 - (embedding <=> query_vector)) >= 0.3
ORDER BY embedding <=> query_vector
LIMIT 5;
```

### Función match_material_chunks

**Uso desde Backend:**

```python
# routers/rag_vector.py

async def get_relevant_chunks(query: str, course_id: str, material_id: str = None):
    """
    Busca chunks relevantes para una consulta.
    """
    # 1. Generar embedding de la pregunta
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query,
        dimensions=1536
    )
    query_embedding = response.data[0].embedding
    
    # 2. Buscar chunks similares
    supabase = get_supabase_client()
    result = supabase.rpc('match_material_chunks', {
        'query_embedding': query_embedding,
        'course_filter': course_id,
        'material_filter': material_id,
        'match_threshold': 0.3,  # Solo chunks con similitud >= 30%
        'match_count': 5         # Top 5
    }).execute()
    
    chunks = result.data
    logger.info(f"Found {len(chunks)} relevant chunks")
    
    return chunks
```

**Ejemplo de Resultado:**

```python
query = "¿Qué normas regulan el cableado estructurado?"
chunks = await get_relevant_chunks(query, course_id, material_id)

# [
#   {
#     "content": "Las principales normas son ANSI/TIA-568 e ISO/IEC 11801...",
#     "similarity": 0.87,
#     "material_title": "Cableado Estructurado",
#     "course_code": "REDES-102",
#     "author": "Dr. García"
#   },
#   {
#     "content": "La norma ANSI/TIA-568 define los estándares para cableado...",
#     "similarity": 0.82,
#     ...
#   },
#   ...
# ]
```

---

## 🤖 Generación de Respuestas

### Construcción del Prompt

**Estrategia:**

1. **System Message:** Define el rol del asistente
2. **Context:** Chunks recuperados como conocimiento
3. **User Query:** Pregunta original del usuario

**Código (routers/rag_vector.py):**

```python
async def generate_answer(query: str, chunks: List[dict]):
    """
    Genera respuesta usando GPT-4 con contexto de chunks.
    """
    # Construir contexto desde chunks
    context_parts = []
    for i, chunk in enumerate(chunks):
        context_parts.append(
            f"[Fuente {i+1}: {chunk['material_title']} - {chunk['course_code']}]\n"
            f"{chunk['content']}\n"
            f"(Similitud: {chunk['similarity']:.2f})"
        )
    
    context = "\n\n---\n\n".join(context_parts)
    
    # Prompt estructurado
    system_prompt = f"""Eres un asistente educativo especializado en responder preguntas sobre materiales de cursos.

CONTEXTO RECUPERADO:
{context}

INSTRUCCIONES:
1. Responde SOLO basándote en el contexto proporcionado
2. Si el contexto no contiene la información, di "No encontré información suficiente"
3. Cita las fuentes cuando sea relevante (ej: "Según el material de Cableado Estructurado...")
4. Sé claro, conciso y educativo
5. Si hay múltiples fuentes con información similar, sintetízalas
"""
    
    # Llamada a OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        temperature=0.7,        # Creatividad moderada
        max_tokens=1000,        # Límite de respuesta
        presence_penalty=0.1,   # Penaliza repetición
        frequency_penalty=0.1
    )
    
    answer = response.choices[0].message.content
    
    return {
        "answer": answer,
        "sources": [
            {
                "material_title": chunk["material_title"],
                "course_code": chunk["course_code"],
                "similarity": chunk["similarity"],
                "content_preview": chunk["content"][:200] + "..."
            }
            for chunk in chunks
        ]
    }
```

### Ejemplo de Conversación

**Input:**

```python
query = "¿Qué velocidades soporta el cable Cat6?"
course_id = "uuid-redes-102"
```

**Chunks Recuperados:**

```python
[
  {
    "content": "El cable Cat6 (Categoría 6) soporta velocidades de hasta 1 Gbps 
                a distancias de 100 metros, y puede alcanzar hasta 10 Gbps en 
                distancias más cortas (hasta 55 metros).",
    "similarity": 0.89,
    "material_title": "Cableado Estructurado",
    "course_code": "REDES-102"
  },
  {
    "content": "Comparado con Cat5e que soporta 1 Gbps, el Cat6 mejora el 
                rendimiento con mayor ancho de banda (250 MHz vs 100 MHz).",
    "similarity": 0.75,
    ...
  }
]
```

**Respuesta Generada:**

```
El cable Cat6 (Categoría 6) soporta velocidades de hasta 1 Gbps a distancias 
de 100 metros. En distancias más cortas (hasta 55 metros), puede alcanzar 
velocidades de hasta 10 Gbps.

Esto representa una mejora significativa sobre el Cat5e, que está limitado a 
1 Gbps. El Cat6 también ofrece mayor ancho de banda (250 MHz comparado con 
100 MHz del Cat5e).

**Fuentes:**
- Material: "Cableado Estructurado" (REDES-102)
- Similitud: 89%
```

---

## ⚡ Optimizaciones

### 1. Threshold Ajustable

**Problema:** Threshold muy alto = pocas respuestas, muy bajo = mucho ruido

**Solución:** Ajustar dinámicamente

```python
async def get_relevant_chunks_adaptive(query, course_id):
    """
    Intenta con threshold alto, si no encuentra baja gradualmente.
    """
    thresholds = [0.7, 0.5, 0.3]
    
    for threshold in thresholds:
        chunks = await search_with_threshold(query, course_id, threshold)
        if len(chunks) >= 3:  # Mínimo 3 chunks
            return chunks
    
    # Si aún no encuentra, retornar los mejores disponibles
    return await search_with_threshold(query, course_id, 0.0)
```

### 2. Caché de Embeddings

**Problema:** Misma pregunta genera embedding múltiples veces

**Solución:** Redis cache

```python
import redis
import hashlib

redis_client = redis.Redis(host='localhost', port=6379)

async def get_embedding_cached(text: str):
    # Hash del texto como key
    cache_key = f"emb:{hashlib.sha256(text.encode()).hexdigest()}"
    
    # Intentar obtener desde cache
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Si no está en cache, generar
    embedding = await generate_embedding(text)
    
    # Guardar en cache (TTL 1 hora)
    redis_client.setex(cache_key, 3600, json.dumps(embedding))
    
    return embedding
```

### 3. Batch Processing de PDFs

**Problema:** Procesar PDFs uno por uno es lento

**Solución:** Background tasks con Celery (futuro)

```python
from celery import Celery

celery_app = Celery('edurag', broker='redis://localhost:6379')

@celery_app.task
def process_pdf_async(file_path, material_id, course_id):
    """
    Procesa PDF en background.
    """
    result = process_pdf_material(file_path, material_id, course_id)
    return result

# En el endpoint
@router.post("/materials/upload")
async def upload_material(file: UploadFile):
    # Guardar archivo
    file_path = save_file(file)
    
    # Crear registro
    material = create_material_record(file_path)
    
    # Procesar en background
    process_pdf_async.delay(file_path, material.id, material.course_id)
    
    return {"message": "Processing started", "material_id": material.id}
```

### 4. Reranking

**Problema:** Similitud vectorial no siempre es perfecta

**Solución:** Reordenar resultados con modelo especializado

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank_chunks(query: str, chunks: List[dict]):
    """
    Reordena chunks usando cross-encoder.
    """
    # Crear pares query-chunk
    pairs = [[query, chunk["content"]] for chunk in chunks]
    
    # Calcular scores
    scores = reranker.predict(pairs)
    
    # Reordenar por score
    for chunk, score in zip(chunks, scores):
        chunk["rerank_score"] = float(score)
    
    chunks.sort(key=lambda x: x["rerank_score"], reverse=True)
    
    return chunks
```

---

## 🔗 Próximo Documento

Finaliza con [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) para aprender a desplegar el sistema en producción.

---

*Última actualización: Octubre 23, 2025*
*Versión: 1.0.0*
