# Diagrama de Arquitectura - Proyecto EduRAG

## Información del Documento

**Curso:** Análisis de Sistemas II  
**Proyecto:** EduRAG - Sistema de Gestión Educativa con IA  
**Tipo de Documento:** Arquitectura del Sistema  
**Fecha:** Octubre 2025

---

## 1. Introducción

Este documento presenta la arquitectura completa del sistema EduRAG mediante diagramas visuales y descripciones detalladas. La arquitectura está diseñada siguiendo el patrón **Cliente-Servidor de 3 Capas** con integración de servicios externos de Inteligencia Artificial.

---

## 2. Arquitectura General del Sistema

### 2.1 Diagrama de Arquitectura de Alto Nivel

```mermaid
graph TB
    subgraph "Capa de Presentación"
        A[Usuario Web Browser]
        B[Vue 3 SPA<br/>Frontend Application]
    end
    
    subgraph "Capa de Lógica de Negocio"
        C[FastAPI Backend<br/>API REST Server]
        D[Routers<br/>students, courses, materials, RAG]
        E[Services<br/>PDF Processor, RAG Engine]
    end
    
    subgraph "Capa de Datos"
        F[(PostgreSQL + pgvector<br/>Database)]
        G[Supabase Storage<br/>PDF Files]
    end
    
    subgraph "Servicios Externos"
        H[OpenAI API<br/>GPT-4o-mini + Embeddings]
    end
    
    A -->|HTTP/HTTPS| B
    B -->|REST API<br/>JSON| C
    C --> D
    D --> E
    E -->|SQL Queries| F
    E -->|Upload/Download| G
    E -->|API Calls| H
    H -->|Embeddings<br/>Responses| E
    F -->|Results| E
    G -->|Files| E
    E -->|JSON| D
    D -->|JSON Response| C
    C -->|JSON| B
    B -->|Render HTML/CSS| A
    
    style A fill:#e1f5ff
    style B fill:#bbdefb
    style C fill:#fff9c4
    style D fill:#fff59d
    style E fill:#fff176
    style F fill:#c8e6c9
    style G fill:#a5d6a7
    style H fill:#ffccbc
```

**Descripción del Diagrama:**

Este diagrama muestra la arquitectura general del sistema dividida en 3 capas principales más servicios externos:

1. **Capa de Presentación (Frontend):**
   - Usuario interactúa con navegador web.
   - Vue 3 SPA maneja toda la interfaz de usuario.
   - Comunicación vía HTTP/HTTPS.

2. **Capa de Lógica de Negocio (Backend):**
   - FastAPI servidor procesa todas las peticiones.
   - Routers manejan endpoints específicos.
   - Services contienen lógica compleja (procesamiento de PDFs, RAG).

3. **Capa de Datos:**
   - PostgreSQL almacena datos estructurados y vectores.
   - Supabase Storage almacena archivos PDF.

4. **Servicios Externos:**
   - OpenAI API proporciona capacidades de IA.

---

### 2.2 Diagrama de Arquitectura Detallada por Componentes

```mermaid
graph TB
    subgraph "Frontend - Vue 3"
        A[Router<br/>Vue Router]
        B[Views<br/>AdminView, StudentView, DirectorView]
        C[Components<br/>Forms, Tables, Chat]
        D[Services<br/>api.js - Axios Client]
        E[State Management<br/>ref, reactive, computed]
    end
    
    subgraph "Backend - FastAPI"
        F[Main App<br/>main.py]
        G[Routers]
        G1[students.py]
        G2[courses.py]
        G3[instructors.py]
        G4[materials.py]
        G5[enrollments.py]
        G6[rag_vector.py]
        G7[analytics.py]
        H[Services]
        H1[pdf_processor.py]
        H2[storage_service.py]
        I[Models<br/>Pydantic Schemas]
        J[Database Client<br/>Supabase Client]
    end
    
    subgraph "Database - Supabase"
        K[(PostgreSQL)]
        K1[students]
        K2[courses]
        K3[instructors]
        K4[materials]
        K5[enrollments]
        K6[material_chunks]
        L[Storage Buckets]
        L1[course-materials]
    end
    
    subgraph "External Services"
        M[OpenAI API]
        M1[text-embedding-3-small]
        M2[gpt-4o-mini]
    end
    
    A --> B
    B --> C
    C --> D
    D -->|HTTP POST/GET/PUT/DELETE| F
    F --> G
    G --> G1 & G2 & G3 & G4 & G5 & G6 & G7
    G1 & G2 & G3 & G4 & G5 & G6 & G7 --> H
    H --> H1 & H2
    G --> I
    G & H --> J
    J --> K
    K --> K1 & K2 & K3 & K4 & K5 & K6
    H2 --> L
    L --> L1
    H1 --> M
    G6 --> M
    M --> M1 & M2
    
    style A fill:#90caf9
    style B fill:#64b5f6
    style C fill:#42a5f5
    style D fill:#2196f3
    style E fill:#1976d2
    style F fill:#fff59d
    style G fill:#fff176
    style H fill:#ffee58
    style I fill:#ffeb3b
    style J fill:#fdd835
    style K fill:#81c784
    style L fill:#66bb6a
    style M fill:#ff8a65
```

**Descripción de Componentes:**

**Frontend (Vue 3):**
- **Router**: Gestiona navegación entre vistas (`/admin`, `/student`, `/director`).
- **Views**: Vistas principales para cada rol.
- **Components**: Componentes reutilizables (formularios, tablas, chat).
- **Services**: Capa de comunicación con backend (Axios).
- **State Management**: Gestión reactiva de estado con Composition API.

**Backend (FastAPI):**
- **Main App**: Punto de entrada, configuración CORS, lifespan events.
- **Routers**: 7 routers modulares, uno por entidad/funcionalidad.
- **Services**: Lógica compleja separada (procesamiento PDFs, RAG).
- **Models**: Validación de datos con Pydantic.
- **Database Client**: Singleton para conexión a Supabase.

**Database (Supabase):**
- **PostgreSQL**: 6 tablas relacionales + extensión pgvector.
- **Storage**: Bucket para almacenar PDFs.

**External Services:**
- **OpenAI API**: 2 modelos (embeddings + chat).

---

## 3. Flujo de Datos por Módulo

### 3.1 Flujo CRUD Básico (Ejemplo: Crear Estudiante)

```mermaid
sequenceDiagram
    participant U as Usuario
    participant F as Frontend<br/>(Vue)
    participant B as Backend<br/>(FastAPI)
    participant D as Database<br/>(PostgreSQL)
    
    U->>F: 1. Llena formulario de estudiante
    U->>F: 2. Clic "Guardar"
    F->>F: 3. Valida campos en frontend
    F->>B: 4. POST /api/students<br/>{nombre, email, etc.}
    B->>B: 5. Valida con Pydantic
    B->>D: 6. INSERT INTO students
    D-->>B: 7. ID generado + registro
    B-->>F: 8. 201 Created<br/>{id, nombre, email, created_at}
    F->>F: 9. Actualiza tabla de estudiantes
    F-->>U: 10. Mensaje "Estudiante creado exitosamente"
```

**Descripción del Flujo:**

1. **Usuario** llena formulario con datos del estudiante.
2. **Usuario** envía formulario haciendo clic en "Guardar".
3. **Frontend** realiza validación básica (campos requeridos, formato email).
4. **Frontend** envía petición HTTP POST a backend con JSON.
5. **Backend** valida datos usando modelo Pydantic `StudentCreate`.
6. **Backend** ejecuta query SQL `INSERT` en tabla `students`.
7. **Database** retorna ID generado y datos insertados.
8. **Backend** responde con código 201 (Created) y JSON del estudiante.
9. **Frontend** actualiza lista de estudiantes en interfaz.
10. **Frontend** muestra mensaje de éxito al usuario.

---

### 3.2 Flujo Completo de Procesamiento de Material (PDF)

```mermaid
sequenceDiagram
    participant U as Administrador
    participant F as Frontend
    participant B as Backend
    participant S as Supabase<br/>Storage
    participant P as PDF Processor<br/>Service
    participant O as OpenAI API
    participant D as PostgreSQL<br/>+ pgvector
    
    U->>F: 1. Selecciona PDF y curso
    U->>F: 2. Clic "Subir Material"
    F->>B: 3. POST /api/materials<br/>(multipart/form-data)
    B->>S: 4. Upload PDF
    S-->>B: 5. URL del archivo
    B->>D: 6. INSERT INTO materials<br/>(status='pending')
    B-->>F: 7. 201 Created<br/>"Material cargado, procesando..."
    F-->>U: 8. Mensaje de éxito
    
    Note over B,P: Procesamiento Asíncrono
    P->>S: 9. Download PDF
    S-->>P: 10. PDF bytes
    P->>P: 11. Extract text (pdfplumber)
    P->>P: 12. Split into chunks<br/>(LangChain, 500 chars, 50 overlap)
    
    loop Para cada chunk
        P->>O: 13. Generate embedding
        O-->>P: 14. Vector 1536 dims
        P->>D: 15. INSERT INTO material_chunks<br/>(content, embedding)
    end
    
    P->>D: 16. UPDATE materials<br/>status='completed', chunks_count=N
    
    Note over U,D: Usuario puede consultar estado después
```

**Descripción del Flujo:**

**Fase 1: Carga del PDF (Síncrona)**
1. Administrador selecciona archivo PDF y curso destino.
2. Administrador inicia carga haciendo clic en "Subir Material".
3. Frontend envía petición multipart/form-data a backend.
4. Backend sube PDF a Supabase Storage.
5. Storage retorna URL del archivo almacenado.
6. Backend inserta registro en tabla `materials` con `status='pending'`.
7. Backend responde inmediatamente al frontend (no espera procesamiento).
8. Usuario recibe confirmación de carga exitosa.

**Fase 2: Procesamiento (Asíncrona en segundo plano)**
9. PDF Processor descarga archivo desde Storage.
10. Storage retorna bytes del PDF.
11. Processor extrae texto usando pdfplumber.
12. Processor divide texto en chunks de ~500 caracteres con overlap de 50.
13-14. Para cada chunk, genera embedding usando OpenAI (vector de 1536 dimensiones).
15. Inserta chunk con su embedding en tabla `material_chunks`.
16. Actualiza material con `status='completed'` y contador de chunks.

**Resultado:** PDF procesado y listo para búsqueda vectorial en chat.

---

### 3.3 Flujo Completo del Sistema RAG (Chat Inteligente)

```mermaid
sequenceDiagram
    participant E as Estudiante
    participant F as Frontend
    participant B as Backend<br/>(RAG Router)
    participant O as OpenAI API
    participant D as PostgreSQL<br/>+ pgvector
    
    E->>F: 1. Selecciona curso
    E->>F: 2. Escribe pregunta y envía
    F->>B: 3. POST /api/rag/chat<br/>{question, course_id}
    
    Note over B,O: Fase 1: Generar Embedding de Pregunta
    B->>O: 4. Generate embedding<br/>(text-embedding-3-small)
    O-->>B: 5. Query vector (1536 dims)
    
    Note over B,D: Fase 2: Búsqueda Vectorial
    B->>D: 6. SELECT match_material_chunks()<br/>(cosine similarity, threshold=0.3)
    D->>D: 7. Vector search con HNSW index
    D-->>B: 8. Top 5 chunks relevantes<br/>(content + similarity scores)
    
    alt Chunks relevantes encontrados (similarity >= 0.3)
        Note over B: Fase 3a: Construir Prompt con Contexto
        B->>B: 9. Concatenar chunks en contexto
        B->>B: 10. Construir prompt estructurado
        
        Note over B,O: Fase 4a: Generar Respuesta con LLM
        B->>O: 11. Chat completion<br/>(gpt-4o-mini, prompt + contexto)
        O-->>B: 12. Respuesta generada
        B-->>F: 13. 200 OK<br/>{answer: "respuesta contextualizada"}
    else No hay chunks relevantes (similarity < 0.3)
        Note over B: Fase 3b: Respuesta predefinida
        B-->>F: 14. 200 OK<br/>{answer: "No encontré información relevante"}
    end
    
    F->>F: 15. Agregar respuesta a historial de chat
    F-->>E: 16. Mostrar respuesta en interfaz
```

**Descripción Detallada del Flujo RAG:**

**Paso 1-3: Iniciación**
- Estudiante selecciona curso para contextualizar chat.
- Estudiante escribe pregunta en lenguaje natural.
- Frontend envía pregunta y course_id a endpoint RAG.

**Fase 1: Vectorización de Pregunta (Pasos 4-5)**
- Backend envía pregunta a OpenAI para generar embedding.
- OpenAI retorna vector de 1536 dimensiones que representa semánticamente la pregunta.
- **Modelo usado:** `text-embedding-3-small`
- **Costo:** ~$0.02 por 1M tokens

**Fase 2: Búsqueda Vectorial (Pasos 6-8)**
- Backend llama función SQL `match_material_chunks` con:
  - Query embedding (vector de pregunta)
  - Course ID (para filtrar solo chunks del curso)
  - Threshold de similitud (0.3)
  - Número de resultados (5)
- PostgreSQL usa índice HNSW para búsqueda rápida.
- Calcula similitud coseno entre query vector y embeddings de chunks.
- Retorna top 5 chunks con similarity >= 0.3.
- **Performance:** <100ms con índice HNSW.

**Fase 3a: Construcción de Prompt (Pasos 9-10)** [Si hay chunks relevantes]
- Backend concatena contenido de los 5 chunks.
- Construye prompt estructurado:
  ```
  Eres un asistente educativo. Responde basándote en el siguiente contexto del curso [Nombre]:
  
  Contexto:
  [Chunk 1 content]
  [Chunk 2 content]
  [Chunk 3 content]
  [Chunk 4 content]
  [Chunk 5 content]
  
  Pregunta del estudiante:
  [Pregunta original]
  
  Responde en español de manera clara y educativa. Si el contexto no contiene información suficiente, indícalo.
  ```

**Fase 4a: Generación de Respuesta (Pasos 11-12)** [Si hay chunks relevantes]
- Backend envía prompt a OpenAI GPT-4o-mini.
- **Parámetros:**
  - `temperature=0.3` (respuestas consistentes, menos creativas)
  - `max_tokens=500` (respuestas concisas)
- GPT-4 genera respuesta basada en contexto proporcionado.
- **Costo:** ~$0.15 por 1M tokens input, ~$0.60 por 1M tokens output.

**Fase 3b/4b: Sin Información (Paso 14)** [Si no hay chunks relevantes]
- Backend detecta que no hay chunks con similarity >= 0.3.
- Retorna mensaje predefinido sin llamar a GPT-4 (ahorro de costos).
- Mensaje: "No encontré información relevante sobre tu pregunta en el material del curso."

**Pasos 15-16: Presentación**
- Frontend agrega respuesta a historial de conversación.
- Frontend renderiza respuesta en interfaz de chat.
- Estudiante puede continuar haciendo preguntas.

**Optimizaciones Implementadas:**
- ✅ Índice HNSW para búsquedas vectoriales rápidas.
- ✅ Threshold de similitud para evitar respuestas irrelevantes.
- ✅ No se llama a GPT-4 si no hay contexto relevante.
- ✅ Temperature baja para respuestas consistentes.

---

## 4. Arquitectura de Base de Datos

### 4.1 Diagrama Entidad-Relación (ER)

```mermaid
erDiagram
    STUDENTS ||--o{ ENROLLMENTS : "inscrito_en"
    COURSES ||--o{ ENROLLMENTS : "tiene"
    COURSES ||--o{ MATERIALS : "contiene"
    INSTRUCTORS ||--o{ COURSES : "imparte"
    MATERIALS ||--o{ MATERIAL_CHUNKS : "dividido_en"
    
    STUDENTS {
        uuid id PK
        varchar first_name
        varchar last_name
        varchar email UK
        date birth_date
        timestamp created_at
    }
    
    INSTRUCTORS {
        uuid id PK
        varchar first_name
        varchar last_name
        varchar email UK
        varchar specialty
        timestamp created_at
    }
    
    COURSES {
        uuid id PK
        varchar name
        varchar code UK
        text description
        int credits
        uuid instructor_id FK
        timestamp created_at
    }
    
    MATERIALS {
        uuid id PK
        varchar name
        text description
        uuid course_id FK
        varchar file_url
        varchar processing_status
        int chunks_count
        timestamp created_at
    }
    
    ENROLLMENTS {
        uuid id PK
        uuid student_id FK
        uuid course_id FK
        varchar status
        timestamp enrolled_at
    }
    
    MATERIAL_CHUNKS {
        uuid id PK
        uuid material_id FK
        text content
        vector_1536 embedding
        int chunk_index
        timestamp created_at
    }
```

**Descripción de Relaciones:**

1. **STUDENTS → ENROLLMENTS (1:N)**
   - Un estudiante puede tener múltiples inscripciones.
   - Una inscripción pertenece a un solo estudiante.
   - **Eliminación:** ON DELETE CASCADE (eliminar estudiante elimina sus inscripciones).

2. **COURSES → ENROLLMENTS (1:N)**
   - Un curso puede tener múltiples inscripciones.
   - Una inscripción pertenece a un solo curso.
   - **Eliminación:** ON DELETE CASCADE.

3. **INSTRUCTORS → COURSES (1:N)**
   - Un instructor puede impartir múltiples cursos.
   - Un curso tiene un solo instructor asignado.
   - **Eliminación:** ON DELETE RESTRICT (no permitir eliminar instructor con cursos).

4. **COURSES → MATERIALS (1:N)**
   - Un curso puede tener múltiples materiales (PDFs).
   - Un material pertenece a un solo curso.
   - **Eliminación:** ON DELETE CASCADE.

5. **MATERIALS → MATERIAL_CHUNKS (1:N)**
   - Un material se divide en múltiples chunks.
   - Un chunk pertenece a un solo material.
   - **Eliminación:** ON DELETE CASCADE (eliminar material elimina sus chunks).

---

### 4.2 Diagrama de Almacenamiento Vectorial

```mermaid
graph LR
    subgraph "Material Original"
        A[PDF Document<br/>50 páginas]
    end
    
    subgraph "Procesamiento"
        B[Text Extraction<br/>pdfplumber]
        C[Text Chunking<br/>LangChain<br/>500 chars, 50 overlap]
    end
    
    subgraph "Vectorización"
        D[Chunk 1<br/>"El cableado estructurado..."]
        E[Chunk 2<br/>"Los estándares TIA/EIA..."]
        F[Chunk 3<br/>"La categoría 6A soporta..."]
        G[...]
        H[Chunk N<br/>"..."]
    end
    
    subgraph "OpenAI API"
        I[text-embedding-3-small]
    end
    
    subgraph "PostgreSQL + pgvector"
        J[(material_chunks table)]
        K[id: uuid<br/>material_id: uuid<br/>content: text<br/>embedding: vector-1536-<br/>chunk_index: int]
        L[HNSW Index<br/>m=16, ef_construction=64]
    end
    
    A --> B
    B --> C
    C --> D & E & F & G & H
    D & E & F & G & H --> I
    I -->|Vector 1536 dims| J
    J --> K
    K --> L
    
    style A fill:#ffccbc
    style B fill:#fff9c4
    style C fill:#fff59d
    style D fill:#c5e1a5
    style E fill:#c5e1a5
    style F fill:#c5e1a5
    style G fill:#c5e1a5
    style H fill:#c5e1a5
    style I fill:#ff8a65
    style J fill:#81c784
    style K fill:#66bb6a
    style L fill:#4caf50
```

**Descripción del Flujo de Vectorización:**

1. **PDF Original:** Documento de 50 páginas con contenido educativo.

2. **Text Extraction:** pdfplumber extrae texto completo del PDF.

3. **Text Chunking:** LangChain divide texto en fragmentos de ~500 caracteres con overlap de 50.

4. **Chunks Individuales:** Se generan N chunks (ejemplo: 51 chunks para PDF típico).

5. **OpenAI Embeddings:** Cada chunk se envía a OpenAI para generar su embedding (vector de 1536 dimensiones).

6. **Almacenamiento en PostgreSQL:**
   - Cada chunk se guarda en tabla `material_chunks`.
   - Incluye: contenido original (text) + embedding (vector).

7. **Índice HNSW:** Se crea índice especializado para búsquedas vectoriales rápidas.

**Ventajas del Almacenamiento Vectorial:**
- ✅ Búsqueda semántica (por significado, no solo keywords).
- ✅ Búsquedas muy rápidas con índice HNSW (<100ms).
- ✅ Escalable hasta 100K+ chunks sin degradación.

---

## 5. Arquitectura de Seguridad

### 5.1 Diagrama de Flujo de Seguridad

```mermaid
graph TB
    subgraph "Frontend - Browser"
        A[Usuario ingresa<br/>credenciales]
        B[Vue App]
    end
    
    subgraph "Backend - FastAPI"
        C[Login Endpoint<br/>/api/auth/login]
        D[Validación de<br/>credenciales]
        E[Generación de<br/>sesión/token]
    end
    
    subgraph "Database"
        F[(users table)]
    end
    
    subgraph "Protecciones"
        G[CORS Policy<br/>Allow: localhost:5173, *.edurag.com]
        H[Pydantic Validation<br/>Email format, required fields]
        I[Environment Variables<br/>.env file]
        J[HTTPS en producción<br/>SSL/TLS]
    end
    
    A --> B
    B -->|POST credentials| C
    C --> H
    H --> D
    D --> F
    F --> D
    D --> E
    E -->|Session/Token| C
    C -->|Response| B
    B --> A
    
    G -.protege.-> C
    I -.configura.-> C
    J -.encripta.-> B
    
    style A fill:#e1f5ff
    style B fill:#bbdefb
    style C fill:#fff9c4
    style D fill:#fff59d
    style E fill:#fff176
    style F fill:#c8e6c9
    style G fill:#ffcdd2
    style H fill:#ef9a9a
    style I fill:#e57373
    style J fill:#f44336
```

**Capas de Seguridad Implementadas:**

1. **CORS (Cross-Origin Resource Sharing):**
   - Configurado en backend para permitir solo orígenes específicos.
   - Desarrollo: `localhost:5173`, `localhost:8000`.
   - Producción: Solo dominio oficial del sistema.

2. **Validación de Datos (Pydantic):**
   - Todos los inputs validados en backend.
   - Formatos de email, tipos de datos, rangos.
   - Previene inyecciones SQL y datos malformados.

3. **Variables de Entorno:**
   - Credenciales sensibles nunca en código fuente.
   - Archivo `.env` para desarrollo (no en Git).
   - Variables de entorno en producción (Render/Railway).

4. **HTTPS/TLS en Producción:**
   - Todo el tráfico encriptado.
   - Certificados SSL de Let's Encrypt (gratis).
   - Previene man-in-the-middle attacks.

5. **Supabase Security:**
   - Row Level Security (RLS) si se configura.
   - API Keys con permisos limitados.
   - Conexiones encriptadas a base de datos.

---

## 6. Arquitectura de Despliegue

### 6.1 Diagrama de Despliegue en Producción

```mermaid
graph TB
    subgraph "Usuarios Finales"
        A[Usuarios Web<br/>Browsers]
    end
    
    subgraph "CDN / Edge Network"
        B[Vercel / Netlify<br/>Frontend Hosting]
    end
    
    subgraph "Backend Hosting - Render.com"
        C[Gunicorn Server<br/>4 Workers]
        D[Uvicorn Workers<br/>FastAPI Apps]
    end
    
    subgraph "Supabase Cloud"
        E[(PostgreSQL 15<br/>+ pgvector)]
        F[Supabase Storage<br/>PDFs]
    end
    
    subgraph "External Services"
        G[OpenAI API<br/>Embeddings + Chat]
    end
    
    subgraph "Monitoring & Logs"
        H[Render Logs]
        I[Supabase Dashboard]
    end
    
    A -->|HTTPS| B
    B -->|Static Assets<br/>HTML/CSS/JS| A
    A -->|API Calls<br/>HTTPS| C
    C --> D
    D -->|SSL Connection| E
    D -->|HTTPS| F
    D -->|HTTPS API Calls| G
    C --> H
    E --> I
    
    style A fill:#e1f5ff
    style B fill:#80deea
    style C fill:#fff59d
    style D fill:#fff176
    style E fill:#81c784
    style F fill:#66bb6a
    style G fill:#ff8a65
    style H fill:#ffab91
    style I fill:#ffccbc
```

**Descripción del Despliegue:**

**Frontend:**
- **Hosting:** Vercel o Netlify (edge network global).
- **Build:** `npm run build` genera assets estáticos.
- **Deploy:** Automático desde Git push.
- **CDN:** Assets servidos desde edge locations cercanos al usuario.
- **HTTPS:** Certificado SSL automático.

**Backend:**
- **Hosting:** Render.com (containers en cloud).
- **Server:** Gunicorn con 4 workers.
- **Workers:** Uvicorn workers ejecutando FastAPI.
- **Health Checks:** Endpoint `/` para monitoring.
- **Logs:** Centralizados en Render dashboard.

**Base de Datos:**
- **Hosting:** Supabase Cloud (PostgreSQL managed).
- **Backups:** Automáticos diarios.
- **Conexiones:** Connection pooling automático.
- **Seguridad:** Conexiones SSL/TLS.

**Storage:**
- **Hosting:** Supabase Storage (S3-compatible).
- **Acceso:** URLs firmadas con expiración.
- **Bucket:** `course-materials` para PDFs.

**Servicios Externos:**
- **OpenAI:** Llamadas HTTPS a api.openai.com.
- **Rate Limiting:** Manejo de límites de API.

---

## 7. Patrones Arquitectónicos Aplicados

### 7.1 Patrón de Capas (Layered Architecture)

```mermaid
graph TB
    subgraph "Presentation Layer"
        A[Vue Components<br/>UI Logic]
    end
    
    subgraph "Application Layer"
        B[FastAPI Routers<br/>Request Handling]
    end
    
    subgraph "Business Logic Layer"
        C[Services<br/>PDF Processing, RAG Engine]
    end
    
    subgraph "Data Access Layer"
        D[Database Client<br/>Supabase Client]
    end
    
    subgraph "Database Layer"
        E[(PostgreSQL<br/>Persistent Storage)]
    end
    
    A -->|API Calls| B
    B -->|Calls| C
    C -->|Queries| D
    D -->|SQL| E
    E -->|Results| D
    D -->|Data| C
    C -->|Response| B
    B -->|JSON| A
```

**Beneficios del Patrón de Capas:**
- ✅ **Separación de Responsabilidades:** Cada capa tiene un propósito claro.
- ✅ **Mantenibilidad:** Cambios en una capa no afectan otras.
- ✅ **Testabilidad:** Cada capa se puede probar independientemente.
- ✅ **Escalabilidad:** Capas pueden escalar horizontalmente.

---

### 7.2 Patrón Cliente-Servidor

```mermaid
graph LR
    A[Cliente<br/>Vue SPA<br/>Browser] <-->|HTTP/HTTPS<br/>REST API| B[Servidor<br/>FastAPI<br/>Backend]
    B <-->|SQL| C[(Database<br/>PostgreSQL)]
    B <-->|API Calls| D[External Services<br/>OpenAI]
```

**Características:**
- **Cliente:** Frontend Vue 3 ejecutándose en browser del usuario.
- **Servidor:** Backend FastAPI en servidor remoto.
- **Comunicación:** HTTP/HTTPS con JSON (REST API).
- **Separación:** Cliente y servidor son aplicaciones independientes.

---

### 7.3 Patrón Repository (Implícito)

Aunque no está explícitamente implementado como clases Repository, el patrón se sigue implícitamente:

```python
# Abstracción de acceso a datos centralizada en routers
@router.get("/students")
async def get_students():
    response = supabase.table('students').select("*").execute()
    return response.data

# En lugar de queries dispersas en todo el código
```

---

## 8. Escalabilidad de la Arquitectura

### 8.1 Estrategias de Escalabilidad

```mermaid
graph TB
    subgraph "Escalabilidad Horizontal"
        A[Load Balancer]
        B[Backend Instance 1]
        C[Backend Instance 2]
        D[Backend Instance N]
    end
    
    subgraph "Escalabilidad Vertical"
        E[Upgrade CPU/RAM<br/>Database Server]
    end
    
    subgraph "Caching Layer - Futuro"
        F[Redis Cache<br/>Embeddings, Respuestas]
    end
    
    subgraph "Database Optimization"
        G[Connection Pooling]
        H[HNSW Indexes]
        I[Query Optimization]
    end
    
    A --> B & C & D
    B & C & D --> G
    G --> E
    E --> H & I
    F -.cache.-> B & C & D
```

**Implementado Actualmente:**
- ✅ **Connection Pooling:** Supabase gestiona pool de conexiones.
- ✅ **HNSW Indexes:** Búsquedas vectoriales optimizadas.
- ✅ **Async/Await:** FastAPI soporta miles de requests concurrentes.

**Futuras Mejoras:**
- 🔮 **Redis Cache:** Cachear embeddings y respuestas frecuentes.
- 🔮 **Horizontal Scaling:** Múltiples instancias de backend con load balancer.
- 🔮 **Database Replication:** Read replicas para queries pesadas.

---

## 9. Resiliencia y Tolerancia a Fallos

### 9.1 Puntos de Fallo y Mitigaciones

| Componente | Punto de Fallo Potencial | Mitigación Implementada |
|------------|--------------------------|-------------------------|
| **Frontend** | Browser crash | Estado en memoria se pierde (aceptable para MVP) |
| **Backend** | Server crash | Restart automático en Render, health checks |
| **Database** | Connection loss | Retry logic en cliente Supabase |
| **OpenAI API** | Rate limit exceeded | Retry con exponential backoff |
| **OpenAI API** | Service unavailable | Error handling, mensaje al usuario |
| **Storage** | File upload fails | Error handling, retry mechanism |

**Estrategias de Resiliencia:**
- ✅ **Try-Catch:** Todos los endpoints tienen manejo de excepciones.
- ✅ **Health Checks:** Endpoint `/` retorna status del servidor.
- ✅ **Logging:** Errores registrados para debugging.
- ✅ **Graceful Degradation:** Sistema funciona parcialmente si OpenAI falla.

---

## 10. Conclusiones de Arquitectura

### 10.1 Fortalezas de la Arquitectura

✅ **Modular y Mantenible:**
- Separación clara de capas y responsabilidades.
- Fácil agregar nuevas funcionalidades sin afectar existentes.

✅ **Escalable:**
- Arquitectura preparada para crecimiento horizontal.
- Índices optimizados para grandes volúmenes de datos.

✅ **Moderna:**
- Uso de tecnologías actuales (FastAPI async, Vue 3, pgvector).
- Siguiendo best practices de la industria.

✅ **Bien Documentada:**
- Diagramas claros de arquitectura.
- Flujos documentados paso a paso.

### 10.2 Consideraciones Futuras

🔮 **Microservicios (Opcional):**
- Separar procesamiento de PDFs en servicio independiente.
- Motor RAG como microservicio.

🔮 **Message Queue:**
- Usar RabbitMQ o Kafka para procesamiento asíncrono de PDFs.
- Mejor manejo de workloads pesados.

🔮 **Containerización:**
- Dockerizar backend y frontend.
- Facilitar despliegue y consistencia de entornos.

---

**Documento de Diagrama de Arquitectura - EduRAG**  
**Análisis de Sistemas II**  
**Octubre 2025**  
**Estado: Arquitectura Completa y Documentada** ✅
