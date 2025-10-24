# 🗄️ Arquitectura de Base de Datos - EduRAG

## 📋 Contenido

1. [Esquema de Base de Datos](#esquema-de-base-de-datos)
2. [pgvector Extension](#pgvector-extension)
3. [Funciones SQL Personalizadas](#funciones-sql-personalizadas)
4. [Índices y Performance](#índices-y-performance)
5. [Relaciones y Constraints](#relaciones-y-constraints)

---

## 🗃️ Esquema de Base de Datos

### Diagrama ER

```
┌──────────────┐         ┌──────────────┐
│  students    │         │   courses    │
├──────────────┤         ├──────────────┤
│ id (PK)      │         │ id (PK)      │
│ name         │         │ code (UNIQUE)│
│ email (UQ)   │         │ name         │
│ cohort       │         │ description  │
│ created_at   │         │ created_at   │
└──────┬───────┘         └──────┬───────┘
       │                        │
       │  ┌─────────────────────┤
       │  │                     │
       ▼  ▼                     ▼
┌──────────────┐         ┌──────────────┐
│ enrollments  │         │  materials   │
├──────────────┤         ├──────────────┤
│ id (PK)      │         │ id (PK)      │
│ student_id   │◄────┐   │ course_id FK │
│ course_id FK │     │   │ title        │
│ status       │     │   │ file_path    │
│ enroll_date  │     │   │ author       │
└──────────────┘     │   │ status       │
                     │   │ chunks_count │
                     │   └──────┬───────┘
                     │          │
                     │          ▼
                     │   ┌──────────────────┐
                     │   │material_chunks   │
                     │   ├──────────────────┤
                     │   │ id (PK)          │
                     └───┤ material_id FK   │
                         │ course_id FK     │
                         │ chunk_index      │
                         │ content TEXT     │
                         │ embedding VECTOR │
                         └──────────────────┘
```

---

## 📊 Tablas Detalladas

### 1. students

```sql
CREATE TABLE students (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    cohort VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_students_email ON students(email);
CREATE INDEX idx_students_cohort ON students(cohort);
CREATE INDEX idx_students_created_at ON students(created_at DESC);

-- Comentarios
COMMENT ON TABLE students IS 'Estudiantes registrados en el sistema';
COMMENT ON COLUMN students.cohort IS 'Cohorte del estudiante (ej: 2024-A, 2024-B)';
```

**Decisiones de Diseño:**

- **UUID vs SERIAL:** UUID previene enumeration attacks y es único globalmente
- **Email UNIQUE:** Un estudiante = un email
- **TIMESTAMP WITH TIME ZONE:** Importante para sistemas multi-timezone

### 2. courses

```sql
CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE UNIQUE INDEX idx_courses_code ON courses(code);
CREATE INDEX idx_courses_name ON courses USING gin(to_tsvector('spanish', name));

-- Comentarios
COMMENT ON TABLE courses IS 'Cursos académicos disponibles';
COMMENT ON COLUMN courses.code IS 'Código único del curso (ej: BD-101, REDES-102)';
```

**Decisiones:**

- **code UNIQUE:** Identificador humano-legible
- **GIN index en name:** Full-text search en español
- **description TEXT:** Sin límite para descripciones largas

### 3. materials

```sql
CREATE TABLE materials (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    author VARCHAR(255),
    processing_status VARCHAR(50) DEFAULT 'pending' CHECK (processing_status IN ('pending', 'processing', 'completed', 'failed')),
    chunks_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_materials_course_id ON materials(course_id);
CREATE INDEX idx_materials_status ON materials(processing_status);
CREATE INDEX idx_materials_created_at ON materials(created_at DESC);

-- Comentarios
COMMENT ON TABLE materials IS 'Materiales (PDFs) subidos por curso';
COMMENT ON COLUMN materials.processing_status IS 'Estado del procesamiento: pending, processing, completed, failed';
COMMENT ON COLUMN materials.chunks_count IS 'Número de chunks generados del PDF';
```

**Decisiones:**

- **ON DELETE CASCADE:** Eliminar material elimina sus chunks
- **CHECK constraint:** Solo valores válidos en processing_status
- **chunks_count:** Desnormalizado para performance (evita COUNT en chunks)

### 4. material_chunks

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE material_chunks (
    id BIGSERIAL PRIMARY KEY,
    material_id UUID NOT NULL REFERENCES materials(id) ON DELETE CASCADE,
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(1536),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(material_id, chunk_index)
);

-- Índices
CREATE INDEX idx_chunks_material_id ON material_chunks(material_id);
CREATE INDEX idx_chunks_course_id ON material_chunks(course_id);

-- Índice HNSW para búsqueda vectorial rápida
CREATE INDEX material_chunks_embedding_idx 
ON material_chunks 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Comentarios
COMMENT ON TABLE material_chunks IS 'Chunks de texto con embeddings para RAG';
COMMENT ON COLUMN material_chunks.embedding IS 'Vector de 1536 dimensiones (OpenAI text-embedding-3-small)';
COMMENT ON INDEX material_chunks_embedding_idx IS 'Índice HNSW para búsqueda por similitud de coseno';
```

**Decisiones:**

- **BIGSERIAL:** Pueden haber millones de chunks
- **VECTOR(1536):** Dimensión fija de OpenAI embeddings
- **HNSW index:** Algoritmo más rápido para búsqueda ANN (Approximate Nearest Neighbors)
- **m=16, ef_construction=64:** Parámetros balanceados para velocidad/precisión

### 5. enrollments

```sql
CREATE TABLE enrollments (
    id SERIAL PRIMARY KEY,
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'completed')),
    enrollment_date DATE DEFAULT CURRENT_DATE,
    UNIQUE(student_id, course_id)
);

-- Índices
CREATE INDEX idx_enrollments_student_id ON enrollments(student_id);
CREATE INDEX idx_enrollments_course_id ON enrollments(course_id);
CREATE INDEX idx_enrollments_status ON enrollments(status);
CREATE INDEX idx_enrollments_date ON enrollments(enrollment_date DESC);

-- Comentarios
COMMENT ON TABLE enrollments IS 'Inscripciones de estudiantes en cursos';
COMMENT ON CONSTRAINT enrollments_student_id_course_id_key ON enrollments IS 'Un estudiante no puede inscribirse dos veces en el mismo curso';
```

**Decisiones:**

- **UNIQUE(student_id, course_id):** Evita inscripciones duplicadas
- **ON DELETE CASCADE:** Eliminar estudiante elimina sus inscripciones
- **status CHECK:** Solo valores válidos

---

## 🔍 pgvector Extension

### ¿Qué es pgvector?

**pgvector** es una extensión de PostgreSQL que añade soporte nativo para:

- Tipo de dato `VECTOR(n)` para almacenar arrays de floats
- Operadores de similitud (coseno, L2, inner product)
- Índices especializados (IVFFlat, HNSW) para búsqueda rápida

### Instalación

```sql
-- Habilitar extensión (Supabase lo hace automático)
CREATE EXTENSION IF NOT EXISTS vector;

-- Verificar instalación
SELECT * FROM pg_extension WHERE extname = 'vector';
```

### Operadores de Similitud

```sql
-- Similitud de coseno (0 = opuestos, 1 = idénticos)
SELECT 1 - (embedding <=> query_vector) AS cosine_similarity
FROM material_chunks;

-- Distancia L2 (Euclidiana)
SELECT embedding <-> query_vector AS l2_distance
FROM material_chunks;

-- Producto interno (Inner product)
SELECT embedding <#> query_vector AS inner_product
FROM material_chunks;
```

**Elegimos coseno porque:**
- Invariante a magnitud (solo importa dirección)
- Estándar en NLP y embeddings
- Rango [0,1] más intuitivo que distancias

### Índices HNSW

**HNSW (Hierarchical Navigable Small World)** es un algoritmo de grafos para búsqueda aproximada de vecinos más cercanos.

**Parámetros:**

```sql
CREATE INDEX ON material_chunks
USING hnsw (embedding vector_cosine_ops)
WITH (
    m = 16,                -- Máximo de conexiones por nodo (trade-off velocidad/memoria)
    ef_construction = 64   -- Tamaño de lista de candidates durante construcción
);
```

**Trade-offs:**

| Parámetro | Bajo | Alto |
|-----------|------|------|
| m | + Rápido, - Preciso | - Rápido, + Preciso |
| ef_construction | + Rápido build, - Preciso | - Rápido build, + Preciso |

**Valores elegidos (m=16, ef=64):**
- Balance óptimo para datasets medianos (<1M vectores)
- Build rápido (<30s para 10K vectores)
- Recall ~95% (encuentra 95% de verdaderos vecinos)

### Performance de HNSW

**Sin índice (full scan):**
```sql
-- O(n) - escanea todos los registros
SELECT * FROM material_chunks
ORDER BY embedding <=> query_vector
LIMIT 5;
-- Tiempo: ~500ms para 10K registros
```

**Con índice HNSW:**
```sql
-- O(log n) - salta a regiones relevantes
SELECT * FROM material_chunks
ORDER BY embedding <=> query_vector
LIMIT 5;
-- Tiempo: ~5ms para 10K registros (100x más rápido)
```

---

## 🔧 Funciones SQL Personalizadas

### match_material_chunks

**Propósito:** Búsqueda vectorial con metadatos (joins automáticos)

**Código Completo:**

```sql
CREATE OR REPLACE FUNCTION match_material_chunks(
    query_embedding VECTOR(1536),
    course_filter UUID DEFAULT NULL,
    material_filter UUID DEFAULT NULL,
    match_threshold FLOAT DEFAULT 0.3,
    match_count INT DEFAULT 5
)
RETURNS TABLE(
    id BIGINT,
    material_id UUID,
    course_id UUID,
    content TEXT,
    similarity FLOAT,
    course_code TEXT,
    course_name TEXT,
    material_title TEXT,
    author TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        mc.id,
        mc.material_id,
        mc.course_id,
        mc.content,
        -- Similitud de coseno (1 - distancia)
        (1 - (mc.embedding <=> query_embedding))::FLOAT AS similarity,
        -- Metadatos desde joins
        c.code::TEXT AS course_code,
        c.name::TEXT AS course_name,
        m.title::TEXT AS material_title,
        COALESCE(m.author, 'Unknown')::TEXT AS author
    FROM material_chunks mc
    INNER JOIN courses c ON mc.course_id = c.id
    INNER JOIN materials m ON mc.material_id = m.id
    WHERE
        -- Filtro de curso (opcional)
        (course_filter IS NULL OR mc.course_id = course_filter)
        AND
        -- Filtro de material (opcional)
        (material_filter IS NULL OR mc.material_id = material_filter)
        AND
        -- Threshold de similitud
        (1 - (mc.embedding <=> query_embedding)) >= match_threshold
    ORDER BY
        -- Ordenar por similitud descendente
        mc.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Comentario
COMMENT ON FUNCTION match_material_chunks IS 
'Búsqueda vectorial de chunks con metadatos. Retorna chunks más similares al query_embedding con información de curso y material.';
```

### Uso desde Backend

```python
# Python con Supabase client
result = supabase.rpc('match_material_chunks', {
    'query_embedding': embedding_vector,  # Lista de 1536 floats
    'course_filter': course_uuid,         # Opcional: filtrar por curso
    'material_filter': None,              # Opcional: filtrar por material
    'match_threshold': 0.3,               # Solo chunks con similitud >= 0.3
    'match_count': 5                      # Máximo 5 resultados
}).execute()

chunks = result.data
# [
#   {
#     "id": 123,
#     "content": "El cableado estructurado...",
#     "similarity": 0.87,
#     "course_code": "REDES-102",
#     "material_title": "Cableado Estructurado",
#     "author": "Dr. García"
#   },
#   ...
# ]
```

### Ventajas de Función SQL vs Query Manual

**Función SQL:**
```python
# 1 round-trip al servidor
result = supabase.rpc('match_material_chunks', params).execute()
```

**Query manual:**
```python
# 3 round-trips
chunks = supabase.table("material_chunks").select("*").execute()
courses = supabase.table("courses").select("*").execute()
materials = supabase.table("materials").select("*").execute()
# Joins manuales en Python...
```

---

## ⚡ Índices y Performance

### Índices Creados

```sql
-- Estudiantes
CREATE INDEX idx_students_email ON students(email);              -- LOGIN lookup
CREATE INDEX idx_students_cohort ON students(cohort);            -- GROUP BY cohort
CREATE INDEX idx_students_created_at ON students(created_at);    -- ORDER BY recent

-- Cursos
CREATE UNIQUE INDEX idx_courses_code ON courses(code);           -- UNIQUE constraint
CREATE INDEX idx_courses_name_fts ON courses                     -- Full-text search
    USING gin(to_tsvector('spanish', name));

-- Materiales
CREATE INDEX idx_materials_course_id ON materials(course_id);    -- JOIN con courses
CREATE INDEX idx_materials_status ON materials(processing_status); -- WHERE status = ...
CREATE INDEX idx_materials_created_at ON materials(created_at);  -- ORDER BY recent

-- Chunks
CREATE INDEX idx_chunks_material_id ON material_chunks(material_id); -- JOIN
CREATE INDEX idx_chunks_course_id ON material_chunks(course_id);     -- FILTER by course
CREATE INDEX material_chunks_embedding_idx ON material_chunks        -- VECTOR SEARCH
    USING hnsw (embedding vector_cosine_ops);

-- Inscripciones
CREATE INDEX idx_enrollments_student_id ON enrollments(student_id);  -- JOIN
CREATE INDEX idx_enrollments_course_id ON enrollments(course_id);    -- JOIN
CREATE INDEX idx_enrollments_status ON enrollments(status);          -- FILTER
CREATE INDEX idx_enrollments_date ON enrollments(enrollment_date);   -- ORDER BY
```

### Query Planning

**Verificar uso de índices:**

```sql
EXPLAIN ANALYZE
SELECT * FROM students WHERE email = 'juan@example.com';

-- Resultado esperado:
-- Index Scan using idx_students_email on students (cost=0.15..8.17 rows=1)
--   Index Cond: (email = 'juan@example.com'::text)
--   Execution Time: 0.123 ms
```

**Sin índice:**
```
Seq Scan on students (cost=0.00..35.50 rows=1)
  Filter: (email = 'juan@example.com'::text)
  Execution Time: 2.456 ms
```

---

## 🔗 Relaciones y Constraints

### Foreign Keys

```sql
-- materials → courses
ALTER TABLE materials
ADD CONSTRAINT fk_materials_course
FOREIGN KEY (course_id) REFERENCES courses(id)
ON DELETE CASCADE;

-- material_chunks → materials
ALTER TABLE material_chunks
ADD CONSTRAINT fk_chunks_material
FOREIGN KEY (material_id) REFERENCES materials(id)
ON DELETE CASCADE;

-- material_chunks → courses
ALTER TABLE material_chunks
ADD CONSTRAINT fk_chunks_course
FOREIGN KEY (course_id) REFERENCES courses(id)
ON DELETE CASCADE;

-- enrollments → students
ALTER TABLE enrollments
ADD CONSTRAINT fk_enrollments_student
FOREIGN KEY (student_id) REFERENCES students(id)
ON DELETE CASCADE;

-- enrollments → courses
ALTER TABLE enrollments
ADD CONSTRAINT fk_enrollments_course
FOREIGN KEY (course_id) REFERENCES courses(id)
ON DELETE CASCADE;
```

### ON DELETE CASCADE

**Cascada automática:**

```sql
-- Eliminar curso elimina:
DELETE FROM courses WHERE id = 'xxx';
-- ✓ Todos los materials del curso
-- ✓ Todos los material_chunks del curso
-- ✓ Todas las enrollments del curso
```

**Sin CASCADE:**
```sql
-- Error: violates foreign key constraint
DELETE FROM courses WHERE id = 'xxx';
-- ✗ Debe eliminar materials primero
-- ✗ Debe eliminar chunks primero
-- ✗ Debe eliminar enrollments primero
```

### CHECK Constraints

```sql
-- Solo valores válidos en status
ALTER TABLE materials
ADD CONSTRAINT check_materials_status
CHECK (processing_status IN ('pending', 'processing', 'completed', 'failed'));

ALTER TABLE enrollments
ADD CONSTRAINT check_enrollments_status
CHECK (status IN ('active', 'inactive', 'completed'));

-- Chunks count no negativo
ALTER TABLE materials
ADD CONSTRAINT check_materials_chunks_count
CHECK (chunks_count >= 0);
```

---

## 📈 Monitoreo y Mantenimiento

### Estadísticas de Tablas

```sql
-- Tamaño de tablas
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Vacuum y Analyze

```sql
-- Reclamar espacio y actualizar estadísticas
VACUUM ANALYZE material_chunks;

-- Auto-vacuum (configurado en Supabase)
SELECT relname, last_vacuum, last_autovacuum, last_analyze
FROM pg_stat_user_tables;
```

---

## 🔗 Próximo Documento

Continúa con [RAG_IMPLEMENTATION.md](RAG_IMPLEMENTATION.md) para entender cómo se implementa el sistema RAG completo.

---

*Última actualización: Octubre 23, 2025*
*Versión: 1.0.0*
