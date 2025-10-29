# 🤖 EduRAG Telegram Bot - Guía de Configuración Completa

## 📋 Índice
1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Prerrequisitos](#prerrequisitos)
3. [Configuración del Backend](#configuración-del-backend)
4. [Configuración de Supabase](#configuración-de-supabase)
5. [Creación del Bot de Telegram](#creación-del-bot-de-telegram)
6. [Configuración de n8n](#configuración-de-n8n)
7. [Pruebas y Validación](#pruebas-y-validación)
8. [Troubleshooting](#troubleshooting)

---

## 🏗️ Arquitectura del Sistema

```
Profesor (Usuario)
    ↓ Telegram
Bot de Telegram (@edurag_assistant_bot)
    ↓ Webhook
n8n Workflow
    ↓ HTTP Requests
Backend API (Render)
    ├→ GET /api/evaluations/pending
    ├→ GET /api/materials/{id}
    ├→ GET /api/materials/{id}/download
    ├→ POST /api/evaluations
    └→ Supabase Database + Storage
    ↓ OpenAI API
gpt-4o-mini (análisis y calificación)
```

**Comandos del Bot:**
- `/pendientes` - Lista materiales sin calificar
- `/calificar [ID]` - Califica un material específico
- `/help` - Muestra ayuda

**Flujo de Calificación:**
1. Profesor envía `/pendientes` → Recibe lista de materiales
2. Profesor copia ID del material
3. Profesor envía `/calificar abc123...`
4. Bot descarga PDF → OpenAI analiza → Guarda calificación → Responde con resultado

---

## ✅ Prerrequisitos

### Servicios Necesarios
- ✅ Backend desplegado en Render (https://edurag-zpil.onrender.com)
- ✅ Frontend desplegado en Vercel (https://edu-rag-pc2d.vercel.app)
- ✅ Base de datos Supabase configurada
- ⏳ Cuenta de Telegram
- ⏳ Instancia de n8n (cloud o self-hosted)
- ⏳ API Key de OpenAI (para gpt-4o-mini)

### Herramientas de Desarrollo
- Git
- Python 3.11+ (para desarrollo local)
- Tesseract OCR (para PDFs escaneados)

---

## 🔧 Configuración del Backend

### Paso 1: Instalar Dependencias de OCR

#### En Render (Producción)

Opción A: Usar Dockerfile (Recomendado)

Crea `edurag/backend/Dockerfile.render`:

```dockerfile
FROM python:3.11-slim

# Instalar Tesseract y dependencias del sistema
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    tesseract-ocr-eng \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

En Render Dashboard:
1. Ve a tu servicio backend
2. Settings → Build & Deploy
3. Cambia de "Python" a "Docker"
4. Build Command: `docker build -f Dockerfile.render -t edurag-backend .`
5. Start Command: (vacío, usa CMD del Dockerfile)

Opción B: Buildpack (Alternativa)

Crea `edurag/backend/Aptfile`:

```
tesseract-ocr
tesseract-ocr-spa
tesseract-ocr-eng
poppler-utils
```

En Render Dashboard:
1. Settings → Environment
2. Add Build Command:
   ```bash
   pip install -r requirements.txt && apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-spa tesseract-ocr-eng poppler-utils
   ```

#### En Local (Desarrollo)

**Windows:**
```powershell
# Descargar e instalar Tesseract desde:
# https://github.com/UB-Mannheim/tesseract/wiki

# Agregar a PATH:
# C:\Program Files\Tesseract-OCR\

# Verificar instalación
tesseract --version

# Instalar dependencias Python
cd edurag/backend
pip install -r requirements.txt
```

**macOS:**
```bash
brew install tesseract
brew install tesseract-lang  # Para idiomas adicionales
pip install -r requirements.txt
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-spa tesseract-ocr-eng poppler-utils
pip install -r requirements.txt
```

### Paso 2: Verificar Instalación de OCR

Ejecuta este script Python:

```python
from app.services.ocr_service import check_ocr_availability

result = check_ocr_availability()
print(result)
```

Resultado esperado:
```json
{
  "ocr_available": true,
  "tesseract_installed": true,
  "pdf2image_installed": true,
  "tesseract_version": "5.x.x",
  "languages": ["eng", "spa"]
}
```

### Paso 3: Verificar Nuevos Endpoints

Prueba los endpoints en Render:

```bash
# 1. Ver materiales pendientes
curl https://edurag-zpil.onrender.com/api/evaluations/pending

# 2. Obtener info de un material
curl https://edurag-zpil.onrender.com/api/evaluations/material/{material_id}

# 3. Descargar PDF (debería devolver archivo)
curl -O https://edurag-zpil.onrender.com/api/materials/{material_id}/download

# 4. Ver estadísticas
curl https://edurag-zpil.onrender.com/api/evaluations/stats
```

---

## 🗄️ Configuración de Supabase

### Paso 1: Ejecutar Migración SQL

1. Abre Supabase Dashboard
2. Ve a "SQL Editor"
3. Crea nuevo query
4. Copia y pega el contenido de `edurag/backend/sql/create_evaluations.sql`
5. Click en "Run" (RUN)

### Paso 2: Verificar Creación de Tablas

```sql
-- Verificar tabla de evaluaciones
SELECT * FROM material_evaluations LIMIT 5;

-- Verificar función de materiales pendientes
SELECT * FROM get_pending_evaluations(10);

-- Verificar columna nueva en materials
SELECT id, title, evaluation_status FROM materials LIMIT 5;

-- Verificar estadísticas
SELECT * FROM get_evaluation_stats();
```

### Paso 3: Configurar Políticas de Seguridad (RLS)

```sql
-- Habilitar RLS para nueva tabla
ALTER TABLE material_evaluations ENABLE ROW LEVEL SECURITY;

-- Política: Permitir lectura a usuarios autenticados
CREATE POLICY "Enable read access for authenticated users"
ON material_evaluations FOR SELECT
TO authenticated
USING (true);

-- Política: Permitir inserción a usuarios autenticados
CREATE POLICY "Enable insert for authenticated users"
ON material_evaluations FOR INSERT
TO authenticated
WITH CHECK (true);

-- Política: Permitir eliminación al creador
CREATE POLICY "Enable delete for evaluation creator"
ON material_evaluations FOR DELETE
TO authenticated
USING (evaluated_by = auth.jwt() ->> 'email');
```

### Paso 4: Crear Datos de Prueba (Opcional)

```sql
-- Insertar evaluación de ejemplo
INSERT INTO material_evaluations (
  material_id,
  evaluated_by,
  score,
  coherence_score,
  structure_score,
  strengths,
  improvements,
  ai_model,
  ai_analysis,
  pdf_type
)
VALUES (
  (SELECT id FROM materials LIMIT 1),  -- Primer material
  'test_user',
  8.5,
  9.0,
  8.0,
  ARRAY['Excelente claridad', 'Buena estructura'],
  ARRAY['Agregar más ejemplos', 'Ampliar conclusiones'],
  'gpt-4o-mini',
  '{"raw_response": "test"}'::jsonb,
  'digital'
);

-- Verificar inserción
SELECT * FROM evaluation_summary;
```

---

## 📱 Creación del Bot de Telegram

### Paso 1: Crear Bot con BotFather

1. Abre Telegram
2. Busca `@BotFather`
3. Envía `/newbot`
4. Nombre del bot: `EduRAG Assistant Bot`
5. Username: `edurag_assistant_bot` (debe terminar en "bot")

**Respuesta de BotFather:**
```
Done! Congratulations on your new bot. You will find it at t.me/edurag_assistant_bot.
You can now add a description, about section and profile picture.

Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789

Keep your token secure and store it safely, it can be used by anyone to control your bot.
```

⚠️ **IMPORTANTE:** Guarda el token en un lugar seguro.

### Paso 2: Configurar Bot

```
# Enviar a @BotFather:

/setdescription @edurag_assistant_bot
Bot de evaluación automática de materiales educativos con IA. 
Califica PDFs usando criterios de coherencia y estructura.

/setabouttext @edurag_assistant_bot
Sistema educativo RAG con calificación automática mediante inteligencia artificial.

/setcommands @edurag_assistant_bot
pendientes - Ver materiales pendientes de calificación
calificar - Calificar un material específico
help - Mostrar ayuda y comandos disponibles
```

### Paso 3: Probar Bot

1. Busca tu bot: `@edurag_assistant_bot`
2. Presiona "Start"
3. Envía `/help`
4. Deberías ver el mensaje de ayuda (una vez que n8n esté configurado)

---

## ⚙️ Configuración de n8n

### Paso 1: Instalar n8n

**Opción A: n8n Cloud (Recomendado para producción)**
1. Ve a https://n8n.io/cloud
2. Crea cuenta
3. Crea nueva instancia

**Opción B: Docker (Local/Self-hosted)**
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

**Opción C: npm (Local)**
```bash
npm install -g n8n
n8n start
```

### Paso 2: Configurar Credenciales

#### 2.1 Telegram Bot API

1. En n8n: Settings → Credentials
2. Click "Add Credential"
3. Busca "Telegram"
4. Selecciona "Telegram Bot API"
5. Pega el token de BotFather
6. Nombre: "Telegram Bot API"
7. Save

#### 2.2 OpenAI API

1. Obtén API key de https://platform.openai.com/api-keys
2. En n8n: Add Credential → "OpenAI"
3. Pega API key
4. Nombre: "OpenAI API"
5. Save

### Paso 3: Importar Workflow

1. En n8n: Click "Add Workflow"
2. Click menú (⋮) → Import from File
3. Selecciona `edurag/n8n_telegram_grading_workflow.json`
4. Click "Import"

### Paso 4: Configurar Nodos

#### 4.1 Telegram Trigger

1. Doble click en "Telegram Trigger"
2. Credential: Selecciona "Telegram Bot API"
3. Updates: ✅ message
4. Save

#### 4.2 AI Grading (OpenAI)

1. Doble click en "AI Grading (OpenAI)"
2. Credential: Selecciona "OpenAI API"
3. Model: `gpt-4o-mini`
4. Temperature: `0.3` (más determinista)
5. Max Tokens: `500`
6. Save

**NOTA IMPORTANTE:** El nodo actual tiene un placeholder para el texto del PDF. En producción real, necesitas primero llamar a un endpoint del backend que extraiga el texto con OCR.

**Solución:**

Agrega un nodo HTTP Request antes del nodo OpenAI:

```json
{
  "parameters": {
    "method": "POST",
    "url": "https://edurag-zpil.onrender.com/api/materials/extract-text",
    "sendBody": true,
    "specifyBody": "json",
    "jsonBody": "={{ JSON.stringify({ material_id: $('Extract Material ID').item.json.materialId }) }}"
  },
  "name": "Extract PDF Text with OCR",
  "type": "n8n-nodes-base.httpRequest"
}
```

Luego modifica el mensaje de OpenAI para usar:
```
{{ $('Extract PDF Text with OCR').item.json.text }}
```

#### 4.3 Verificar URLs del Backend

En cada nodo HTTP Request, verifica que la URL sea:
```
https://edurag-zpil.onrender.com
```

### Paso 5: Activar Workflow

1. Click en "Active" (toggle en la esquina superior derecha)
2. El workflow debe cambiar a estado "Active"
3. Telegram Trigger registrará el webhook automáticamente

### Paso 6: Verificar Webhook

```bash
# Verificar que el webhook esté configurado
curl https://api.telegram.org/bot{YOUR_TOKEN}/getWebhookInfo

# Resultado esperado:
{
  "ok": true,
  "result": {
    "url": "https://your-n8n-instance.com/webhook/...",
    "has_custom_certificate": false,
    "pending_update_count": 0
  }
}
```

---

## 🧪 Pruebas y Validación

### Prueba 1: Comando /help

1. Abre Telegram
2. Busca `@edurag_assistant_bot`
3. Envía: `/help`

**Resultado Esperado:**
```
🤖 EduRAG Bot - Ayuda

Comandos disponibles:

/pendientes - Ver materiales sin calificar
/calificar [ID] - Calificar un material específico
/help - Mostrar esta ayuda

Ejemplo de uso:
1️⃣ Escribe /pendientes para ver la lista
2️⃣ Copia el ID del material que quieres calificar
3️⃣ Escribe /calificar [ID]

✨ Características:
• Calificación automática con IA
• Soporte para PDFs escaneados (OCR)
• Evaluación de coherencia y estructura
• Retroalimentación constructiva

💡 Sistema educativo RAG integrado
```

### Prueba 2: Listar Materiales Pendientes

1. Sube un PDF desde el frontend (https://edu-rag-pc2d.vercel.app)
2. En Telegram, envía: `/pendientes`

**Resultado Esperado:**
```
📚 Materiales Pendientes de Calificación

1. Introducción a Python
   📖 Curso: Programación Básica
   📅 Subido: 15/01/2024
   🆔 ID: abc123-def456-ghi789

2. Estructuras de Datos
   📖 Curso: Algoritmos
   📅 Subido: 14/01/2024
   🆔 ID: xyz789-uvw456-rst123

💡 Para calificar un material usa:
/calificar [ID]

Ejemplo: /calificar abc123-def456-ghi789
```

### Prueba 3: Calificar Material

1. Copia un ID de la lista anterior
2. Envía: `/calificar abc123-def456-ghi789`

**Proceso Esperado:**
- Bot confirma: "⏳ Descargando PDF..."
- "🤖 Analizando contenido..."
- "💾 Guardando evaluación..."

**Resultado Esperado:**
```
✅ Calificación Guardada

📄 Introducción a Python

📊 Calificación Final: 8.5/10
   • Coherencia: 9.0/10
   • Estructura: 8.0/10

💪 Fortalezas:
1. Excelente uso de ejemplos prácticos
2. Conceptos explicados de manera clara
3. Código bien documentado

📈 Áreas de Mejora:
1. Agregar más ejercicios de práctica
2. Ampliar la sección de conclusiones
3. Incluir referencias bibliográficas

🤖 Evaluado con: gpt-4o-mini
👤 Por: @tu_username
```

### Prueba 4: Verificar en Supabase

```sql
-- Ver evaluaciones recientes
SELECT 
  e.id,
  m.title,
  e.score,
  e.evaluated_by,
  e.evaluated_at
FROM material_evaluations e
JOIN materials m ON e.material_id = m.id
ORDER BY e.evaluated_at DESC
LIMIT 10;

-- Ver estadísticas
SELECT * FROM get_evaluation_stats();
```

### Prueba 5: Verificar en Dashboard Web

1. Abre https://edu-rag-pc2d.vercel.app
2. Login como profesor
3. Ve a Analytics
4. Deberías ver las calificaciones recientes

---

## 🔍 Debugging en n8n

### Ver Logs de Ejecución

1. En n8n: Click "Executions"
2. Selecciona una ejecución reciente
3. Revisa cada nodo:
   - ✅ Verde = Éxito
   - ❌ Rojo = Error
   - ⏸️ Gris = No ejecutado

### Inspeccionar Datos

1. Click en un nodo ejecutado
2. Pestaña "Output Data"
3. Revisa JSON completo

### Errores Comunes

**Error: "Telegram webhook already set"**
```bash
# Solución: Eliminar webhook anterior
curl -X POST https://api.telegram.org/bot{YOUR_TOKEN}/deleteWebhook
```

**Error: "OpenAI API rate limit"**
- Verifica tu plan de OpenAI
- Reduce la frecuencia de pruebas
- Considera usar gpt-3.5-turbo si gpt-4o-mini no está disponible

**Error: "Material not found"**
- Verifica que el ID es correcto
- Verifica que el material existe en Supabase
- Revisa el endpoint GET /api/materials/{id}

---

## 🛠️ Troubleshooting

### Backend

#### OCR no funciona

```bash
# Verificar instalación de Tesseract
tesseract --version

# Verificar idiomas instalados
tesseract --list-langs

# Instalar idioma español si falta
sudo apt-get install tesseract-ocr-spa  # Linux
brew install tesseract-lang  # macOS
```

#### Endpoint /download falla

```python
# En materials.py, agregar logs
logger.info(f"Downloading from storage: {storage_path}")
logger.info(f"File size: {len(file_data)} bytes")
```

#### Error 500 en /evaluations

```sql
-- Verificar que la función existe
SELECT proname FROM pg_proc WHERE proname = 'get_pending_evaluations';

-- Verificar RLS policies
SELECT * FROM pg_policies WHERE tablename = 'material_evaluations';
```

### n8n

#### Workflow no se activa

1. Verifica que el toggle "Active" esté verde
2. Revisa logs en n8n: Settings → Logs
3. Verifica que el webhook esté registrado en Telegram

#### OpenAI no responde

1. Verifica API key válida
2. Revisa límites de uso en OpenAI Dashboard
3. Prueba con curl:
```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "test"}]
  }'
```

#### Respuesta no llega al usuario

1. Verifica que "Send Telegram Response" está conectado correctamente
2. Revisa que chatId se está pasando correctamente
3. Agrega nodo "Code" antes del Send para debuggear:
```javascript
console.log("ChatId:", $json.chatId);
console.log("Message:", $json.message);
return [$input.all()];
```

### Supabase

#### Permisos RLS

```sql
-- Deshabilitar temporalmente para debug
ALTER TABLE material_evaluations DISABLE ROW LEVEL SECURITY;

-- Verificar inserción manual
INSERT INTO material_evaluations (...) VALUES (...);

-- Volver a habilitar
ALTER TABLE material_evaluations ENABLE ROW LEVEL SECURITY;
```

#### Storage no descarga archivos

1. Verifica políticas del bucket:
```sql
-- En Storage → Policies
CREATE POLICY "Public read access"
ON storage.objects FOR SELECT
TO public
USING (bucket_id = 'course-materials');
```

2. Verifica que el archivo existe:
```javascript
const { data, error } = await supabase
  .storage
  .from('course-materials')
  .list()
```

---

## 📊 Monitoreo en Producción

### Logs en Render

```bash
# Ver logs en tiempo real
render logs -f --service edurag-backend

# Filtrar por errores
render logs --service edurag-backend | grep ERROR

# Ver últimas 100 líneas
render logs --service edurag-backend --tail 100
```

### Métricas en n8n

1. Ve a Settings → Metrics
2. Revisa:
   - Ejecuciones totales
   - Tasa de éxito
   - Tiempo promedio de ejecución

### Queries de Análisis en Supabase

```sql
-- Evaluaciones por día
SELECT 
  DATE(evaluated_at) as date,
  COUNT(*) as total_evaluations,
  AVG(score) as avg_score
FROM material_evaluations
GROUP BY DATE(evaluated_at)
ORDER BY date DESC;

-- Evaluadores más activos
SELECT 
  evaluated_by,
  COUNT(*) as total_evaluations,
  AVG(score) as avg_score
FROM material_evaluations
GROUP BY evaluated_by
ORDER BY total_evaluations DESC;

-- Cursos con mejor calificación promedio
SELECT 
  c.name,
  COUNT(e.id) as total_evaluations,
  AVG(e.score) as avg_score
FROM material_evaluations e
JOIN materials m ON e.material_id = m.id
JOIN courses c ON m.course_id = c.id
GROUP BY c.name
ORDER BY avg_score DESC;
```

---

## 🚀 Próximos Pasos

1. **Agregar autenticación:** Limitar bot solo a profesores registrados
2. **Notificaciones push:** Alertar cuando hay nuevos materiales
3. **Reportes semanales:** Enviar resumen de evaluaciones por Telegram
4. **Calificación por lotes:** `/calificar_pendientes 5` para calificar múltiples
5. **Exportar a Excel:** Generar reporte de calificaciones
6. **Multi-idioma:** Soporte para inglés y otros idiomas
7. **Mejora continua:** Fine-tuning del modelo con feedback

---

## 📚 Referencias

- [Documentación de n8n](https://docs.n8n.io/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [OpenAI API](https://platform.openai.com/docs)
- [Supabase Docs](https://supabase.com/docs)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

---

**✨ ¡Sistema listo para producción!**

Si tienes problemas, revisa primero la sección de [Troubleshooting](#troubleshooting) o contacta al equipo de desarrollo.
