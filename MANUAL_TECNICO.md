# 🔧 Manual Técnico de Desarrollo - EduRAG

## 📑 Índice de Documentación Técnica

Este manual técnico está dividido en múltiples documentos especializados para facilitar la navegación y comprensión del proyecto:

1. **[MANUAL_TECNICO.md](MANUAL_TECNICO.md)** (este documento) - Visión general y arquitectura
2. **[docs/BACKEND_DEVELOPMENT.md](docs/BACKEND_DEVELOPMENT.md)** - Desarrollo del backend FastAPI
3. **[docs/FRONTEND_DEVELOPMENT.md](docs/FRONTEND_DEVELOPMENT.md)** - Desarrollo del frontend Vue 3
4. **[docs/DATABASE_ARCHITECTURE.md](docs/DATABASE_ARCHITECTURE.md)** - Arquitectura de base de datos y pgvector
5. **[docs/RAG_IMPLEMENTATION.md](docs/RAG_IMPLEMENTATION.md)** - Implementación del sistema RAG
6. **[docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)** - Guía de despliegue y producción

---

## 🎯 Introducción

**EduRAG** es un sistema de gestión educativa que integra tecnología RAG (Retrieval-Augmented Generation) para proporcionar consultas inteligentes sobre materiales académicos. Este manual técnico documenta las decisiones de arquitectura, patrones de diseño y procesos de desarrollo del proyecto.

### 👥 Audiencia Objetivo

- Desarrolladores que mantendrán o extenderán el proyecto
- Arquitectos de software evaluando el diseño
- Estudiantes aprendiendo sobre sistemas RAG
- Equipos técnicos implementando sistemas similares

### 📋 Prerequisitos de Conocimiento

Para trabajar en este proyecto se recomienda familiaridad con:

- **Backend:** Python 3.11+, FastAPI, async/await, REST APIs
- **Frontend:** JavaScript ES6+, Vue 3, Composition API, Tailwind CSS
- **Base de Datos:** PostgreSQL, SQL avanzado, índices, foreign keys
- **IA/ML:** Conceptos de embeddings, vectores, similitud de coseno
- **DevOps:** Docker (opcional), variables de entorno, APIs externas

---

## 🏗️ Arquitectura General del Sistema

### Vista de Alto Nivel

```
┌─────────────────────────────────────────────────────────────┐
│                         USUARIO                              │
│                    (Navegador Web)                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP/HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Vue 3)                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │ Courses  │  │ Chat RAG │  │Analytics │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Vue Router + State Management              │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ REST API (JSON)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 BACKEND (FastAPI)                            │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                 API Layer (Routers)                   │  │
│  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐   │  │
│  │  │Auth │ │Stud │ │Cours│ │Mater│ │Enroll││ RAG │   │  │
│  │  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Service Layer (Business Logic)           │  │
│  │  ┌──────────────┐         ┌──────────────┐          │  │
│  │  │ PDF Processor│         │   Storage    │          │  │
│  │  │  - Extract   │         │   Manager    │          │  │
│  │  │  - Chunk     │         │  - Upload    │          │  │
│  │  │  - Embed     │         │  - Download  │          │  │
│  │  └──────────────┘         └──────────────┘          │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────┬───────────────────────┬────────────────────────┘
             │                       │
             │                       │
             ▼                       ▼
┌────────────────────────┐  ┌──────────────────────────┐
│   SUPABASE POSTGRESQL  │  │   OPENAI API             │
│   ┌────────────────┐   │  │   ┌──────────────────┐  │
│   │    Tables      │   │  │   │  GPT-4o-mini     │  │
│   │  - students    │   │  │   │  (Chat)          │  │
│   │  - courses     │   │  │   └──────────────────┘  │
│   │  - materials   │   │  │   ┌──────────────────┐  │
│   │  - chunks      │   │  │   │  text-embedding  │  │
│   │  - enrollments │   │  │   │  -3-small        │  │
│   └────────────────┘   │  │   │  (Embeddings)    │  │
│   ┌────────────────┐   │  │   └──────────────────┘  │
│   │   pgvector     │   │  └──────────────────────────┘
│   │  - HNSW Index  │   │
│   │  - Cosine Sim  │   │
│   └────────────────┘   │
│   ┌────────────────┐   │
│   │    Storage     │   │
│   │  - PDF Files   │   │
│   └────────────────┘   │
└────────────────────────┘
```

### Flujo de Datos Principal

#### 1. Carga de Material (Upload Flow)

```
Usuario → Frontend → Backend → Supabase Storage → Registro en DB
                      ↓
                  Background Task
                      ↓
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
   pdfplumber                  OpenAI API
   (Extracción)              (Embeddings)
        │                           │
        └─────────────┬─────────────┘
                      ▼
              material_chunks (DB)
              + vector index
```

#### 2. Consulta RAG (Query Flow)

```
Pregunta Usuario → Frontend → Backend
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
              OpenAI Embed            Supabase RPC
              (Query vector)      (match_material_chunks)
                    │                       │
                    └───────────┬───────────┘
                                ▼
                        Chunks Relevantes
                                │
                                ▼
                          OpenAI GPT-4
                          (Generación)
                                │
                                ▼
                          Respuesta + Fuentes
```

---

## 🎨 Decisiones de Arquitectura

### Patrón Arquitectónico: Cliente-Servidor de 3 Capas

**Razón de Elección:**

- **Separación de Responsabilidades:** Frontend, backend y datos independientes
- **Escalabilidad:** Cada capa puede escalar por separado
- **Mantenibilidad:** Cambios en una capa no afectan a las demás
- **Testing:** Cada capa es testeable de forma aislada

### Backend: Arquitectura por Capas

```
┌──────────────────────────────────┐
│     API Layer (Routers)          │  ← Maneja HTTP requests/responses
├──────────────────────────────────┤
│   Service Layer (Business Logic) │  ← Lógica de negocio reutilizable
├──────────────────────────────────┤
│   Data Access Layer (Database)   │  ← Comunicación con Supabase
└──────────────────────────────────┘
```

**Ventajas:**

- **Desacoplamiento:** Servicios independientes de routers
- **Reutilización:** Misma lógica de negocio en múltiples endpoints
- **Testing:** Mock fácil de capas inferiores
- **Evolución:** Fácil cambiar DB sin modificar lógica de negocio

### Frontend: Arquitectura por Componentes

```
┌──────────────────────────────────┐
│      Views (Pages)               │  ← Páginas completas (routing)
├──────────────────────────────────┤
│   Components (Reusables)         │  ← Botones, forms, cards
├──────────────────────────────────┤
│   Services (API Client)          │  ← Comunicación con backend
├──────────────────────────────────┤
│   State Management (Refs)        │  ← Estado reactivo
└──────────────────────────────────┘
```

**Ventajas:**

- **Composición:** Componentes pequeños y enfocados
- **Reusabilidad:** Componentes en múltiples vistas
- **Mantenibilidad:** Cambios localizados
- **Performance:** Reactivity system optimizado de Vue 3

---

## 💻 Elección de Tecnologías

### Backend: ¿Por qué FastAPI?

**Alternativas Consideradas:** Flask, Django, Express.js, Spring Boot

**Razones de Elección:**

1. **Performance Nativa:**
   - Basado en Starlette (async/await)
   - Comparable a Node.js y Go
   - Ideal para operaciones I/O intensivas (DB, OpenAI API)

2. **Documentación Automática:**
   - Swagger UI out-of-the-box en `/docs`
   - Reduce tiempo de documentación
   - Facilita testing manual

3. **Validación con Pydantic:**
   - Type hints nativos de Python
   - Validación automática de requests
   - Serialización/deserialización automática
   - Errores claros y específicos

4. **Async/Await:**
   - Crucial para llamadas a OpenAI (3-8 segundos)
   - No bloquea mientras espera respuestas
   - Mejor uso de recursos

5. **Ecosistema Python:**
   - LangChain (chunking)
   - pdfplumber (extracción)
   - OpenAI client nativo
   - Supabase client

**Ejemplo de Valor:**

```python
# Sin FastAPI (Flask)
@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    # Validación manual
    if not data.get('name'):
        return {'error': 'Name required'}, 400
    if not '@' in data.get('email', ''):
        return {'error': 'Invalid email'}, 400
    # ... más validación manual

# Con FastAPI
@router.post("/students")
async def create_student(student: StudentCreate):
    # Validación automática por Pydantic
    # Si llega aquí, datos son válidos
    # student.name y student.email son tipos correctos
```

### Frontend: ¿Por qué Vue 3?

**Alternativas Consideradas:** React, Angular, Svelte

**Razones de Elección:**

1. **Curva de Aprendizaje Suave:**
   - Sintaxis cercana a HTML/CSS/JS vanilla
   - No requiere JSX ni TypeScript obligatorio
   - Ideal para proyectos académicos

2. **Composition API:**
   - Lógica reutilizable con composables
   - Mejor organización que Options API
   - Type inference mejorado

3. **Reactivity System:**
   - Refs y reactive() para estado
   - Actualizaciones automáticas del DOM
   - Performance optimizado

4. **Tamaño del Bundle:**
   - ~30KB gzipped (más ligero que React)
   - Tiempo de carga rápido
   - Mejor UX en conexiones lentas

5. **Ecosistema Maduro:**
   - Vue Router (SPA routing)
   - Vite (build tool ultrarrápido)
   - Tailwind CSS (integración perfecta)

**Ejemplo de Valor:**

```javascript
// React (más verboso)
import { useState, useEffect } from 'react';

function StudentList() {
  const [students, setStudents] = useState([]);
  
  useEffect(() => {
    fetch('/api/students')
      .then(r => r.json())
      .then(setStudents);
  }, []);
  
  return (
    <div>
      {students.map(s => <div key={s.id}>{s.name}</div>)}
    </div>
  );
}

// Vue 3 (más conciso)
<script setup>
import { ref, onMounted } from 'vue';

const students = ref([]);

onMounted(async () => {
  students.value = await (await fetch('/api/students')).json();
});
</script>

<template>
  <div v-for="s in students" :key="s.id">{{ s.name }}</div>
</template>
```

### Base de Datos: ¿Por qué Supabase + PostgreSQL?

**Alternativas Consideradas:** MongoDB + Atlas, MySQL, Firebase, Pinecone

**Razones de Elección:**

1. **pgvector Extension:**
   - Vectores nativos en PostgreSQL
   - Sin necesidad de DB vectorial separada
   - Índices HNSW optimizados
   - Operaciones de similitud eficientes

2. **Relaciones y Consistencia:**
   - Foreign keys para integridad referencial
   - Transacciones ACID
   - Cascadas automáticas
   - Mejor que NoSQL para datos estructurados

3. **Supabase como BaaS:**
   - PostgreSQL gestionado (sin config de servidor)
   - Storage integrado para PDFs
   - Auth ready-to-use (futuro)
   - Dashboard visual
   - API REST auto-generada

4. **Funciones SQL Personalizadas:**
   - RPC para búsqueda vectorial compleja
   - Lógica en DB (mejor performance)
   - Aprovecha optimizador de PostgreSQL

5. **Escalabilidad:**
   - PostgreSQL escala verticalmente bien
   - Réplicas de lectura fáciles
   - Connection pooling incluido

**Comparación con Alternativas:**

| Característica | Supabase+pgvector | Pinecone | MongoDB+Atlas |
|---------------|-------------------|----------|---------------|
| Vectores | ✅ Nativo | ✅ Especializado | ❌ Plugin |
| Relaciones | ✅ Foreign Keys | ❌ No | ⚠️ Referencias |
| Transacciones | ✅ ACID | ❌ No | ⚠️ Limitadas |
| Costo | ✅ Free tier | ❌ Caro | ✅ Free tier |
| Learning curve | ⚠️ Media | ✅ Fácil | ✅ Fácil |
| All-in-one | ✅ DB+Storage+Auth | ❌ Solo vectores | ⚠️ DB+Search |

### IA: ¿Por qué OpenAI?

**Alternativas Consideradas:** Anthropic Claude, Google PaLM, LLaMA local, Cohere

**Razones de Elección:**

1. **GPT-4o-mini:**
   - Balance precio/calidad óptimo
   - $0.15 por 1M input tokens (10x más barato que GPT-4)
   - Respuestas coherentes y precisas
   - Context window de 128K tokens

2. **text-embedding-3-small:**
   - 1536 dimensiones (balance tamaño/precisión)
   - $0.02 por 1M tokens (muy económico)
   - Superior a ada-002 en benchmarks
   - Soporte multilingüe (español)

3. **Ecosistema Maduro:**
   - Documentación excelente
   - Librerías oficiales en Python
   - Rate limits razonables
   - Monitoring en dashboard

4. **Confiabilidad:**
   - 99.9% uptime
   - Latencia consistente (2-4s)
   - Sin necesidad de hosting propio

**Comparación Embeddings:**

| Modelo | Dimensiones | Costo (1M tokens) | MTEB Score |
|--------|-------------|-------------------|------------|
| text-embedding-3-small | 1536 | $0.02 | 62.3% |
| text-embedding-3-large | 3072 | $0.13 | 64.6% |
| ada-002 (legacy) | 1536 | $0.10 | 61.0% |
| Cohere embed-v3 | 1024 | $0.10 | 62.5% |

### Build Tools: ¿Por qué Vite?

**Alternativas Consideradas:** Webpack, Parcel, esbuild

**Razones de Elección:**

1. **Velocidad de Desarrollo:**
   - Hot Module Replacement (HMR) instantáneo
   - Servidor dev arranca en <1 segundo
   - Rebuild incremental rápido

2. **Build de Producción:**
   - Usa Rollup internamente
   - Tree-shaking automático
   - Code splitting inteligente
   - Minificación optimizada

3. **Configuración Mínima:**
   - Zero-config para Vue 3
   - Plugins oficiales
   - Tailwind integración fácil

4. **Soporte Nativo ESM:**
   - Imports ES6 nativos en desarrollo
   - No bundling en dev (faster)

---

## 🔌 Comunicación Entre Componentes

### Protocolo: REST API con JSON

**¿Por qué REST y no GraphQL?**

1. **Simplicidad:** Endpoints claros y predecibles
2. **Caching:** HTTP caching estándar
3. **Tooling:** Swagger UI, Postman, curl
4. **Curva de Aprendizaje:** Más fácil para equipos nuevos

**Estructura de Endpoints:**

```
GET    /api/{resource}         # Listar todos
GET    /api/{resource}/{id}    # Obtener uno
POST   /api/{resource}         # Crear nuevo
PUT    /api/{resource}/{id}    # Actualizar completo
PATCH  /api/{resource}/{id}    # Actualizar parcial (no usado)
DELETE /api/{resource}/{id}    # Eliminar
```

### Formato de Respuestas

**Success (200-201):**
```json
{
  "message": "Operation successful",
  "data": { /* objeto o array */ }
}
```

**Error (400-500):**
```json
{
  "detail": "Descriptive error message"
}
```

### Manejo de Errores

**Frontend:**
```javascript
try {
  const response = await api.post('/students', data);
  showSuccess('Estudiante creado');
} catch (error) {
  if (error.response?.data?.detail) {
    showError(error.response.data.detail);
  } else {
    showError('Error de conexión');
  }
}
```

**Backend:**
```python
@router.get("/{id}")
async def get_student(id: int):
    try:
        result = supabase.table("students").select("*").eq("id", id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Student not found")
        return result.data[0]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 🔒 Seguridad Implementada

### Variables de Entorno

**Configuración:**
```env
# backend/.env
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJxxx...
OPENAI_API_KEY=sk-xxx...
```

**Carga en Backend:**
```python
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not all([SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY]):
    raise ValueError("Missing environment variables")
```

### CORS (Cross-Origin Resource Sharing)

**Configuración en FastAPI:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**¿Por qué CORS?**
- Frontend (5173) y Backend (8000) en puertos diferentes
- Navegador bloquea requests cross-origin por seguridad
- CORS permite explícitamente el acceso

### Validación de Entrada con Pydantic

**Previene:**
- Inyección SQL (Supabase maneja parametrización)
- XSS (no hay HTML rendering en backend)
- Type confusion (int vs string)
- Campos faltantes o inválidos

**Ejemplo:**
```python
class StudentCreate(BaseModel):
    name: str  # Required, must be string
    email: EmailStr  # Required, must be valid email format
    cohort: str  # Required, must be string
    
# Automáticamente rechaza:
# - Requests sin 'name'
# - Emails inválidos como "notanemail"
# - Tipos incorrectos como name = 123
```

### Rate Limiting (OpenAI)

**Implementado por OpenAI:**
- Tier 1: 3,500 RPM (requests per minute)
- Tier 2: 5,000 RPM (con uso)

**Manejo en Código:**
```python
try:
    response = openai.embeddings.create(...)
except openai.RateLimitError:
    logger.warning("Rate limit hit, retrying...")
    await asyncio.sleep(1)
    response = openai.embeddings.create(...)
```

---

## 📊 Performance y Optimización

### Database Indexing

**Índices Creados:**
```sql
-- HNSW para búsqueda vectorial rápida
CREATE INDEX material_chunks_embedding_idx 
ON material_chunks 
USING hnsw (embedding vector_cosine_ops);

-- B-tree para foreign keys (automático)
CREATE INDEX idx_material_chunks_material_id 
ON material_chunks(material_id);

CREATE INDEX idx_enrollments_student_course
ON enrollments(student_id, course_id);
```

**Impacto:**
- Búsqueda vectorial: O(log n) en lugar de O(n)
- Joins con foreign keys: 10-100x más rápido
- Queries de analytics: Subsegundo incluso con miles de registros

### Async Processing en Backend

**Sin Async (Bloqueante):**
```python
def process_pdf(file_path):
    text = extract_text(file_path)  # 2s
    chunks = chunk_text(text)  # 1s
    for chunk in chunks:
        embedding = openai.embed(chunk)  # 0.5s × 50 = 25s
    # Total: 28s bloqueados
```

**Con Async (Non-blocking):**
```python
async def process_pdf(file_path):
    text = await extract_text(file_path)  # 2s
    chunks = chunk_text(text)  # 1s
    
    # Procesar embeddings en paralelo
    tasks = [openai.embed(chunk) for chunk in chunks]
    embeddings = await asyncio.gather(*tasks)  # 5s total
    # Total: 8s (3.5x más rápido)
```

### Frontend Bundle Optimization

**Code Splitting por Ruta:**
```javascript
const routes = [
  {
    path: '/chat',
    component: () => import('./views/ChatRAGView.vue')  // Lazy load
  }
];
```

**Resultado:**
- Bundle inicial: 150KB (en lugar de 500KB)
- Vistas cargadas on-demand
- First Contentful Paint más rápido

### Caching (Futuro)

**Oportunidades:**
```python
# Redis para cache de embeddings de queries frecuentes
cache_key = f"embedding:{query_hash}"
embedding = redis.get(cache_key)
if not embedding:
    embedding = openai.embed(query)
    redis.setex(cache_key, 3600, embedding)  # 1 hora
```

---

## 📁 Estructura de Directorios

```
Proyecto_Final/
├── edurag/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── routers/           # API endpoints
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py        # Autenticación
│   │   │   │   ├── students.py    # CRUD estudiantes
│   │   │   │   ├── courses.py     # CRUD cursos
│   │   │   │   ├── materials.py   # Upload PDFs
│   │   │   │   ├── enrollments.py # Inscripciones
│   │   │   │   ├── rag_vector.py  # Chat RAG
│   │   │   │   └── analytics.py   # Estadísticas
│   │   │   ├── services/          # Business logic
│   │   │   │   ├── __init__.py
│   │   │   │   ├── pdf_processor.py  # Extracción y chunking
│   │   │   │   └── storage.py        # Supabase Storage
│   │   │   ├── core/              # Config
│   │   │   │   ├── __init__.py
│   │   │   │   └── database.py    # Supabase client
│   │   │   └── models/            # Pydantic schemas (futuro)
│   │   ├── sql/                   # Scripts SQL
│   │   │   ├── create_tables.sql
│   │   │   └── create_vector_search_function.sql
│   │   ├── main.py                # Entry point
│   │   ├── requirements.txt       # Dependencias Python
│   │   └── .env                   # Variables de entorno
│   └── frontend/
│       ├── src/
│       │   ├── views/             # Páginas (SPA routes)
│       │   │   ├── DashboardView.vue
│       │   │   ├── AdminView.vue
│       │   │   ├── ChatRAGView.vue
│       │   │   ├── CoursesView.vue
│       │   │   ├── CourseDetailView.vue
│       │   │   ├── CourseManageView.vue
│       │   │   ├── EnrollmentsView.vue
│       │   │   └── AnalyticsView.vue
│       │   ├── components/        # Componentes reutilizables (futuro)
│       │   ├── services/          # API client
│       │   │   └── api.js         # Axios config + endpoints
│       │   ├── router/            # Vue Router
│       │   │   └── index.js
│       │   ├── assets/            # CSS, imágenes
│       │   ├── App.vue            # Root component
│       │   └── main.js            # Entry point
│       ├── public/                # Static assets
│       ├── package.json           # Dependencias npm
│       ├── vite.config.js         # Vite configuration
│       └── tailwind.config.js     # Tailwind CSS
├── docs/                          # Documentación técnica detallada
│   ├── BACKEND_DEVELOPMENT.md
│   ├── FRONTEND_DEVELOPMENT.md
│   ├── DATABASE_ARCHITECTURE.md
│   ├── RAG_IMPLEMENTATION.md
│   └── DEPLOYMENT_GUIDE.md
├── README.md                      # Manual de usuario
├── MANUAL_TECNICO.md             # Este documento
└── ESTADO_PROYECTO.md            # Status report
```

---

## 🔄 Flujo de Desarrollo

### Git Workflow (Recomendado)

```bash
# Feature branches
git checkout -b feature/add-notifications
# ... desarrollo ...
git commit -m "feat: Add push notifications"
git push origin feature/add-notifications
# Pull request → code review → merge to main
```

### Ciclo de Desarrollo Local

**Terminal 1 - Backend:**
```bash
cd edurag/backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
# Auto-reload con uvicorn --reload
```

**Terminal 2 - Frontend:**
```bash
cd edurag/frontend
npm install
npm run dev
# Hot reload automático con Vite
```

**Terminal 3 - Testing:**
```bash
# Backend tests (futuro)
pytest tests/

# Frontend tests (futuro)
npm run test
```

### Debugging

**Backend:**
```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# En código
logger.debug(f"Processing chunk {i}: {chunk[:50]}...")
logger.info(f"PDF processed: {material_id}")
logger.warning(f"Low similarity: {similarity}")
logger.error(f"Failed to generate embedding: {e}")
```

**Frontend:**
```javascript
// Console logs
console.log('Students loaded:', students.value);
console.error('API error:', error);

// Vue DevTools
// Instalar extensión de navegador
// Inspeccionar state, props, emits
```

---

## 🧪 Testing Strategy

### Backend Unit Tests (Futuro)

```python
# tests/test_students.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_student():
    response = client.post("/api/students", json={
        "name": "Test Student",
        "email": "test@example.com",
        "cohort": "2024-A"
    })
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "Test Student"

def test_create_student_invalid_email():
    response = client.post("/api/students", json={
        "name": "Test",
        "email": "not-an-email",
        "cohort": "2024-A"
    })
    assert response.status_code == 422  # Validation error
```

### Integration Tests

```python
def test_rag_flow():
    # 1. Upload PDF
    with open("test.pdf", "rb") as f:
        response = client.post("/api/materials/upload", files={"file": f})
    material_id = response.json()["data"]["id"]
    
    # 2. Wait for processing
    time.sleep(5)
    
    # 3. Query RAG
    response = client.post("/api/rag/chat", json={
        "query": "Test query",
        "material_id": material_id
    })
    assert response.status_code == 200
    assert "answer" in response.json()
```

### Frontend Tests (Futuro)

```javascript
// tests/ChatRAGView.spec.js
import { mount } from '@vue/test-utils';
import ChatRAGView from '@/views/ChatRAGView.vue';

describe('ChatRAGView', () => {
  it('sends query when button clicked', async () => {
    const wrapper = mount(ChatRAGView);
    await wrapper.find('input').setValue('Test query');
    await wrapper.find('button').trigger('click');
    
    expect(wrapper.vm.messages).toHaveLength(2);  // User + AI
  });
});
```

---

## 📚 Referencias y Recursos

### Documentación Oficial

- **FastAPI:** https://fastapi.tiangolo.com/
- **Vue 3:** https://vuejs.org/guide/introduction.html
- **Supabase:** https://supabase.com/docs
- **OpenAI API:** https://platform.openai.com/docs
- **LangChain:** https://python.langchain.com/docs/
- **pgvector:** https://github.com/pgvector/pgvector

### Papers y Artículos

- **RAG:** "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (Lewis et al., 2020)
- **HNSW:** "Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs" (Malkov & Yashunin, 2016)
- **Embeddings:** "Text and Code Embeddings by Contrastive Pre-Training" (OpenAI, 2023)

### Tutoriales Útiles

- FastAPI + Supabase: https://supabase.com/docs/guides/api
- Vue 3 Composition API: https://vuejs.org/api/composition-api-setup.html
- pgvector Setup: https://supabase.com/docs/guides/database/extensions/pgvector

---

## 🎯 Próximos Pasos

Para desarrolladores que continúen este proyecto:

1. **Lee los documentos específicos:**
   - [BACKEND_DEVELOPMENT.md](docs/BACKEND_DEVELOPMENT.md) para backend
   - [FRONTEND_DEVELOPMENT.md](docs/FRONTEND_DEVELOPMENT.md) para frontend
   - [RAG_IMPLEMENTATION.md](docs/RAG_IMPLEMENTATION.md) para sistema RAG

2. **Configura tu entorno:**
   - Sigue [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)

3. **Familiarízate con el código:**
   - Explora `backend/app/routers/` para entender endpoints
   - Revisa `frontend/src/views/` para flujos de usuario
   - Lee `sql/create_vector_search_function.sql` para búsqueda

4. **Experimenta:**
   - Usa `/docs` de FastAPI para probar endpoints
   - Modifica threshold de similitud en RAG
   - Ajusta chunk_size en pdf_processor.py

5. **Contribuye:**
   - Implementa features del roadmap
   - Mejora documentación
   - Añade tests
   - Optimiza performance

---

**Siguiente documento:** [BACKEND_DEVELOPMENT.md →](docs/BACKEND_DEVELOPMENT.md)

---

*Última actualización: Octubre 23, 2025*
*Versión: 1.0.0*
