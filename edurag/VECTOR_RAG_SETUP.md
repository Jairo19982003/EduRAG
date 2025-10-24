# 🚀 Sistema RAG Profesional con Búsqueda Vectorial

## ✅ Implementación Completada

Se ha implementado un sistema RAG (Retrieval Augmented Generation) de nivel profesional con las siguientes características:

### 🎯 Características Principales

1. **Upload de PDFs**: Sube archivos PDF directamente desde la interfaz
2. **Procesamiento Automático**: Extracción de texto + chunking + embeddings
3. **Búsqueda Vectorial**: pgvector con índice HNSW para búsqueda semántica
4. **Respuestas Inteligentes**: OpenAI GPT-4 con contexto relevante
5. **Escalabilidad**: Soporta documentos de cualquier tamaño

---

## 📋 Pasos de Configuración

### PASO 1: Ejecutar SQL de búsqueda vectorial en Supabase

Ya ejecutaste `create_material_chunks.sql`, ahora ejecuta el segundo SQL:

1. Ve a: **Supabase Dashboard → SQL Editor**
2. Crea una nueva consulta
3. Copia el contenido de: `backend/sql/create_vector_search_function.sql`
4. Ejecuta el SQL (Ctrl+Enter)
5. Verifica que se creó la función `match_material_chunks`

```sql
-- Deberías ver este mensaje:
✅ CREATE FUNCTION match_material_chunks
```

### PASO 2: Configurar Supabase Storage

Ejecuta el script de configuración del storage:

```bash
cd backend
python setup_storage.py
```

Este script:
- Crea el bucket `course-materials` en Supabase Storage
- Configura permisos para usuarios autenticados
- Verifica que todo esté listo para uploads

### PASO 3: Verificar que el backend está corriendo

El backend debería reiniciarse automáticamente y cargar los nuevos módulos:

```bash
# Si no está corriendo, inícialo:
cd backend
python main.py
```

Verifica que veas en los logs:
```
INFO: Loading module: app.routers.rag_vector
INFO: Route registered: /api/rag/query
INFO: Route registered: /api/rag/health
INFO: Route registered: /api/materials/upload-pdf
```

### PASO 4: Verificar el frontend

El frontend también debería estar corriendo:

```bash
# Si no está corriendo:
cd frontend
npm run dev
```

---

## 🧪 Probar el Sistema

### 1. Subir un PDF de prueba

1. Ve a: **http://localhost:5173/admin**
2. Click en la pestaña **"Materials"**
3. Llena el formulario:
   - Título: "Ejemplo de PDF"
   - Curso: Selecciona cualquier curso
   - Método de Carga: **"📄 Subir PDF"**
4. Click en el área de upload y selecciona un PDF
5. Click en **"Subir PDF"**

Deberías ver:
```
✅ PDF uploaded successfully. Processing in background...
📊 Tamaño: X.XX MB
⏳ El PDF se está procesando en segundo plano
```

### 2. Verificar el procesamiento

Puedes verificar el estado del procesamiento:

```bash
# En la terminal del backend, deberías ver:
INFO: Starting background PDF processing for material {id}
INFO: PDF processing completed: X chunks created
```

### 3. Hacer una consulta RAG

1. Ve a: **http://localhost:5173/chat-rag**
2. Selecciona el curso donde subiste el PDF
3. Escribe una pregunta sobre el contenido del PDF
4. Click en **"Enviar"**

Deberías recibir una respuesta basada en el contenido del PDF con las fuentes citadas.

---

## 🔍 Arquitectura del Sistema

### Backend

```
backend/
├── app/
│   ├── routers/
│   │   ├── materials.py          ← Upload endpoint
│   │   └── rag_vector.py         ← Vector search + OpenAI
│   └── services/
│       ├── pdf_processor.py      ← Extract, chunk, embed
│       └── storage.py            ← Supabase Storage
├── sql/
│   ├── create_material_chunks.sql           ✅ EJECUTADO
│   └── create_vector_search_function.sql    ⏳ EJECUTAR AHORA
└── main.py                        ← FastAPI app
```

### Frontend

```
frontend/
└── src/
    ├── views/
    │   ├── AdminView.vue          ← PDF upload UI
    │   └── ChatRAGView.vue        ← RAG queries
    └── services/
        └── api.js                 ← API calls
```

### Base de Datos

```sql
-- Tablas principales:
materials              → Metadata de PDFs
material_chunks        → Chunks con embeddings (vector(1536))

-- Índices:
idx_chunks_embedding   → HNSW para búsqueda rápida

-- Funciones:
match_material_chunks  → Búsqueda por similitud
```

---

## 📊 Flujo de Procesamiento de PDFs

```
1. Usuario sube PDF
        ↓
2. Backend: Upload a Supabase Storage
        ↓
3. Guardar metadata en tabla materials
        ↓
4. Background Task inicia:
        ↓
5. pdfplumber extrae texto
        ↓
6. LangChain divide en chunks (500 tokens, 50 overlap)
        ↓
7. OpenAI genera embeddings (1536 dimensiones)
        ↓
8. Guardar chunks en material_chunks
        ↓
9. Actualizar status a "completed"
```

## 🔎 Flujo de Consulta RAG

```
1. Usuario hace pregunta
        ↓
2. Generar embedding de la pregunta
        ↓
3. Buscar chunks similares (pgvector HNSW)
        ↓
4. Recuperar top 5 chunks más relevantes
        ↓
5. Construir prompt con contexto
        ↓
6. OpenAI GPT-4 genera respuesta
        ↓
7. Retornar respuesta + fuentes
```

---

## ⚙️ Configuración Actual

### OpenAI
- **Modelo**: gpt-4o-mini (respuestas)
- **Embeddings**: text-embedding-3-small (1536 dims)
- **Chunk Size**: 500 tokens
- **Chunk Overlap**: 50 tokens
- **Top K**: 5 chunks recuperados
- **Similarity Threshold**: 0.7

### Supabase
- **Database**: PostgreSQL con pgvector
- **Storage**: Bucket `course-materials`
- **Índice**: HNSW (m=16, ef_construction=64)

---

## 🐛 Troubleshooting

### Error: "Table material_chunks does not exist"
**Solución**: Ejecuta `backend/sql/create_material_chunks.sql` en Supabase

### Error: "Function match_material_chunks does not exist"
**Solución**: Ejecuta `backend/sql/create_vector_search_function.sql` en Supabase

### Error: "Bucket course-materials not found"
**Solución**: Ejecuta `python backend/setup_storage.py`

### Error: "OpenAI API key not found"
**Solución**: Verifica que `.env` tenga `OPENAI_API_KEY`

### PDF no se procesa
**Verifica**:
1. Backend logs: ¿Hay errores de procesamiento?
2. Material status: ¿Es "processing" o "failed"?
3. OpenAI API: ¿Hay saldo disponible?

---

## 📈 Próximos Pasos (Opcionales)

- [ ] Agregar indicador de estado en tiempo real
- [ ] Mostrar chunks procesados en AdminView
- [ ] Implementar re-procesamiento de PDFs
- [ ] Agregar soporte para OCR (PDFs escaneados)
- [ ] Implementar límite de rate para uploads

---

## ✅ Checklist de Implementación

- [x] SQL: Tabla material_chunks con vector(1536)
- [x] SQL: Índice HNSW para búsqueda vectorial
- [ ] **SQL: Función match_material_chunks** ← PENDIENTE
- [x] Backend: Servicio de procesamiento PDF
- [x] Backend: Servicio de Supabase Storage
- [x] Backend: Endpoint upload-pdf
- [x] Backend: Router RAG con búsqueda vectorial
- [x] Frontend: UI de upload de PDFs
- [x] Frontend: Selector de modo (PDF vs Texto)
- [ ] **Supabase: Configurar bucket** ← EJECUTAR setup_storage.py
- [ ] Testing: Subir PDF real y hacer consultas

---

## 💡 Consejos

1. **Primeros PDFs**: Empieza con PDFs pequeños (5-10 páginas) para probar
2. **Preguntas específicas**: Las preguntas más específicas obtienen mejores respuestas
3. **Monitoreo**: Revisa los logs del backend para ver el procesamiento
4. **Costos**: Cada PDF genera embeddings (costo en OpenAI API)

---

**¿Listo para probar?**

1. Ejecuta el SQL de la función de búsqueda vectorial
2. Ejecuta `python backend/setup_storage.py`
3. Sube un PDF de prueba en AdminView
4. Haz consultas en ChatRAGView

¡El sistema está listo para usar! 🚀
