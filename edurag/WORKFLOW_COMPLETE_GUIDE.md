# 📖 Guía Completa del Workflow Optimizado - Nodo por Nodo

## 🎯 Índice
1. [Visión General del Flujo](#visión-general-del-flujo)
2. [Explicación Detallada de Cada Nodo](#explicación-detallada-de-cada-nodo)
3. [Prompt del Sistema (IA)](#prompt-del-sistema-ia)
4. [Cómo se Guardan los Datos en Supabase](#cómo-se-guardan-los-datos-en-supabase)
5. [Desencadenamiento del Workflow](#desencadenamiento-del-workflow)
6. [Cómo Probar el Sistema](#cómo-probar-el-sistema)

---

## 📊 Visión General del Flujo

### Diagrama Completo:

```
👤 Usuario envía mensaje en Telegram
    ↓
[1] Telegram Trigger ← Escucha mensajes 24/7
    ↓
[2] Smart Router ← Analiza qué comando es
    ↓
[3] Route Command ← Distribuye según comando
    ↓
┌───────────────┬──────────────────┬─────────────┐
│               │                  │             │
│ /pendientes   │   /calificar     │  /help      │
↓               ↓                  ↓             │
[4] Get Pending [6] Fetch & Prepare [5] (ya formateado)
    ↓               ↓                ↓           │
[5] Format      [7] AI Grading   [5] Format     │
    Response        (OpenAI) 🤖      Response    │
    ↓               ↓                ↓           │
    │           [8] Process &       │           │
    │               Save to DB      │           │
    │               ↓               │           │
    └───────────────┴───────────────┴───────────┘
                    ↓
            [9] Send to Telegram
                    ↓
            📱 Usuario recibe respuesta
```

### Flujo de Datos Simplificado:

```
Telegram → Router → Acción → Formato → Telegram
                      ↓
                   (Si es calificar)
                      ↓
                  Backend → IA → Supabase
```

---

## 🔍 Explicación Detallada de Cada Nodo

### 📱 [1] Telegram Trigger

**Tipo de Nodo:** `n8n-nodes-base.telegramTrigger`

#### ¿Qué hace?
- **Escucha activamente** todos los mensajes enviados al bot de Telegram
- Se mantiene **activo 24/7** esperando comandos
- Registra un **webhook** con Telegram API

#### ¿Cuándo se ejecuta?
- **Cada vez** que un usuario envía un mensaje al bot
- Automáticamente cuando el workflow está **Active**

#### Datos que recibe:
```json
{
  "message": {
    "message_id": 123,
    "from": {
      "id": 987654321,
      "username": "profesor_juan",
      "first_name": "Juan"
    },
    "chat": {
      "id": 987654321,
      "type": "private"
    },
    "text": "/calificar abc123-def456",
    "date": 1730203200
  }
}
```

#### Configuración Requerida:
- **Credential:** Telegram Bot API
  - Token obtenido de @BotFather
  - Formato: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

#### Datos que pasa al siguiente nodo:
```json
{
  "message": { /* objeto completo del mensaje */ }
}
```

---

### 🧠 [2] Smart Router

**Tipo de Nodo:** `n8n-nodes-base.code` (Code Node)

#### ¿Qué hace?
Este es el **cerebro del routing**. Combina TODAS estas funciones:

1. **Extrae información del mensaje:**
   - Texto del comando
   - Chat ID del usuario
   - Username del profesor

2. **Identifica el tipo de comando:**
   - `/help` → Ayuda
   - `/pendientes` → Listar materiales
   - `/calificar [ID]` → Calificar material
   - Otro → Comando desconocido

3. **Valida el formato:**
   - Para `/calificar` verifica que tenga un ID válido
   - ID válido = UUID formato: `abc123-def456-ghi789`

4. **Extrae parámetros:**
   - Si es `/calificar abc123`, extrae `abc123`

5. **Prepara respuestas inmediatas:**
   - Para `/help` genera el mensaje de ayuda
   - Para comandos inválidos genera mensaje de error

#### Código Completo Explicado:

```javascript
// ===== EXTRACCIÓN DE DATOS =====
const message = $input.item.json.message;  // Mensaje completo de Telegram
const text = message.text || '';           // Texto del comando (/help, /calificar, etc)
const chatId = message.chat.id;            // ID único del chat para responder
const username = message.from.username || 'usuario'; // Username del profesor

// ===== DETECCIÓN DE COMANDO /help =====
if (text === '/help') {
  return [
    {
      json: {
        command: 'help',           // Tipo de comando
        chatId: chatId,            // Para saber a quién responder
        message: '🤖 *EduRAG Bot - IA de Calificación*\n\n' +
          '*Comandos:*\n' +
          '📋 `/pendientes` - Ver materiales sin calificar\n' +
          '🤖 `/calificar [ID]` - Calificar con IA\n' +
          '❓ `/help` - Esta ayuda\n\n' +
          '✨ Powered by OpenAI gpt-4o-mini'
      }
    }
  ];
}

// ===== DETECCIÓN DE COMANDO /pendientes =====
if (text === '/pendientes') {
  return [
    {
      json: {
        command: 'pendientes',
        chatId: chatId
        // No necesita más datos, el siguiente nodo hará HTTP request
      }
    }
  ];
}

// ===== DETECCIÓN Y VALIDACIÓN DE /calificar =====
// Regex: /calificar seguido de espacio y UUID
const match = text.match(/^\/calificar\s+([a-f0-9-]+)/i);

if (match) {
  return [
    {
      json: {
        command: 'calificar',
        chatId: chatId,
        materialId: match[1],    // ID extraído del comando
        username: username       // Para guardar quién calificó
      }
    }
  ];
}

// ===== COMANDO DESCONOCIDO =====
return [
  {
    json: {
      command: 'unknown',
      chatId: chatId,
      message: '❌ Comando no reconocido. Usa `/help` para ver comandos.'
    }
  }
];
```

#### Datos de Salida Según Comando:

**Para `/help`:**
```json
{
  "command": "help",
  "chatId": 987654321,
  "message": "🤖 EduRAG Bot..."
}
```

**Para `/pendientes`:**
```json
{
  "command": "pendientes",
  "chatId": 987654321
}
```

**Para `/calificar abc123`:**
```json
{
  "command": "calificar",
  "chatId": 987654321,
  "materialId": "abc123-def456-ghi789",
  "username": "profesor_juan"
}
```

**Para comando inválido:**
```json
{
  "command": "unknown",
  "chatId": 987654321,
  "message": "❌ Comando no reconocido..."
}
```

---

### 🔀 [3] Route Command

**Tipo de Nodo:** `n8n-nodes-base.switch` (Switch Node v3)

#### ¿Qué hace?
- **Distribuye el flujo** según el comando detectado
- Funciona como un **switch/case** en programación
- Tiene **4 salidas** (outputs) posibles

#### Configuración:

```javascript
// Regla 1: Si command == "pendientes"
{
  "conditions": [
    {
      "leftValue": "={{ $json.command }}",
      "operator": "equals",
      "rightValue": "pendientes"
    }
  ],
  "outputKey": "pendientes"  // Sale por output 0
}

// Regla 2: Si command == "calificar"
{
  "conditions": [
    {
      "leftValue": "={{ $json.command }}",
      "operator": "equals",
      "rightValue": "calificar"
    }
  ],
  "outputKey": "calificar"  // Sale por output 1
}

// Regla 3: Si command == "help"
{
  "conditions": [
    {
      "leftValue": "={{ $json.command }}",
      "operator": "equals",
      "rightValue": "help"
    }
  ],
  "outputKey": "help"  // Sale por output 2
}

// Regla 4: Cualquier otro caso (fallback)
{
  "fallbackOutput": "extra"  // Sale por output 3
}
```

#### Rutas de Salida:

| Output | Comando | Va a Nodo |
|--------|---------|-----------|
| 0 | `/pendientes` | **[4] Get Pending** |
| 1 | `/calificar` | **[6] Fetch & Prepare** |
| 2 | `/help` | **[5] Format Response** |
| 3 | Otros | **[5] Format Response** |

---

### 🌐 [4] Get Pending

**Tipo de Nodo:** `n8n-nodes-base.httpRequest` (HTTP Request v4.2)

#### ¿Qué hace?
- Hace una **llamada HTTP GET** al backend en Render
- Obtiene la **lista de materiales pendientes** de calificar
- Consulta el endpoint que lee de Supabase

#### Configuración:

```javascript
{
  "method": "GET",
  "url": "https://edurag-zpil.onrender.com/api/evaluations/pending",
  "sendQuery": true,
  "queryParameters": {
    "parameters": [
      {
        "name": "limit",
        "value": "10"  // Máximo 10 materiales
      }
    ]
  }
}
```

#### URL Completa Generada:
```
https://edurag-zpil.onrender.com/api/evaluations/pending?limit=10
```

#### ¿Qué hace el backend?
El backend (en `edurag/backend/app/routers/evaluations.py`) ejecuta:

```python
@router.get("/pending")
async def get_pending_materials(limit: int = 50):
    # Llama a función SQL en Supabase
    result = supabase.rpc("get_pending_evaluations", {"limit": limit}).execute()
    return result.data
```

#### ¿Qué hace la función SQL?
En Supabase (`create_evaluations.sql`):

```sql
CREATE OR REPLACE FUNCTION get_pending_evaluations(limit_count INTEGER DEFAULT 50)
RETURNS TABLE (
  material_id UUID,
  title VARCHAR,
  course_name VARCHAR,
  uploaded_at TIMESTAMP,
  file_url TEXT
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    m.id,
    m.title,
    c.name as course_name,
    m.created_at,
    m.file_url
  FROM materials m
  LEFT JOIN material_evaluations e ON m.id = e.material_id
  LEFT JOIN courses c ON m.course_id = c.id
  WHERE 
    m.processing_status = 'completed'
    AND m.evaluation_status = 'pending'
    AND e.id IS NULL  -- No tiene evaluación aún
  ORDER BY m.created_at DESC
  LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;
```

#### Datos que Retorna:

```json
[
  {
    "material_id": "abc123-def456-ghi789",
    "title": "Introducción a Python",
    "course_name": "Programación Básica",
    "uploaded_at": "2025-10-20T10:30:00Z",
    "file_url": "course-materials/python-intro.pdf"
  },
  {
    "material_id": "xyz789-uvw456-rst123",
    "title": "Estructuras de Datos",
    "course_name": "Algoritmos",
    "uploaded_at": "2025-10-19T15:20:00Z",
    "file_url": "course-materials/estructuras.pdf"
  }
]
```

#### Siguiente Nodo:
Los datos pasan a **[5] Format Response**

---

### 📝 [5] Format Response

**Tipo de Nodo:** `n8n-nodes-base.code` (Code Node v2)

#### ¿Qué hace?
- **Formatea** cualquier respuesta para que Telegram la entienda
- Convierte arrays JSON en mensajes bonitos con Markdown
- Se reutiliza para múltiples tipos de respuestas

#### Código Completo Explicado:

```javascript
// ===== FORMATEAR LISTA DE MATERIALES PENDIENTES =====
const materials = $input.first().json;  // Puede ser array o ya un mensaje
const chatId = $('Smart Router').first().json.chatId;

// Si ya es un mensaje formateado (de /help o /unknown), pasarlo directo
if (typeof materials === 'object' && materials.message) {
  return {
    json: materials  // Ya tiene chatId y message
  };
}

// Si es lista vacía
if (!materials || materials.length === 0) {
  return {
    json: {
      chatId: chatId,
      message: '✅ No hay materiales pendientes de calificar.'
    }
  };
}

// Si es array de materiales, formatear
let msg = '📚 *Materiales Pendientes*\n\n';

materials.forEach((m, i) => {
  msg += `${i+1}. *${m.title}*\n`;
  msg += `   📖 ${m.course_name}\n`;
  msg += `   🆔 \`${m.material_id}\`\n\n`;
});

msg += '💡 Para calificar: `/calificar [ID]`';

return {
  json: {
    chatId: chatId,
    message: msg
  }
};
```

#### Ejemplo de Output:

Para `/pendientes`:
```json
{
  "chatId": 987654321,
  "message": "📚 *Materiales Pendientes*\n\n1. *Introducción a Python*\n   📖 Programación Básica\n   🆔 `abc123-def456`\n\n💡 Para calificar: `/calificar [ID]`"
}
```

Para `/help`:
```json
{
  "chatId": 987654321,
  "message": "🤖 *EduRAG Bot - IA de Calificación*..."
}
```

#### Siguiente Nodo:
Va directo a **[9] Send to Telegram**

---

### 🔄 [6] Fetch & Prepare

**Tipo de Nodo:** `n8n-nodes-base.code` (Code Node v2)

#### ¿Qué hace?
Este nodo combina **3 operaciones** en una sola:

1. **Obtiene información del material** (HTTP GET)
2. **Envía mensaje de progreso** a Telegram
3. **Prepara el contexto** para el agente de IA

#### Código Completo Explicado:

```javascript
// ===== 1. EXTRACCIÓN DE DATOS DEL ROUTER =====
const materialId = $('Smart Router').first().json.materialId;
const chatId = $('Smart Router').first().json.chatId;

// ===== 2. REQUEST AL BACKEND PARA INFO DEL MATERIAL =====
const materialResponse = await this.helpers.httpRequest({
  method: 'GET',
  url: `https://edurag-zpil.onrender.com/api/materials/${materialId}`,
  json: true  // Parsea respuesta como JSON automáticamente
});

// Si el material no existe
if (!materialResponse) {
  return {
    json: {
      chatId: chatId,
      message: '❌ Material no encontrado',
      error: true
    }
  };
}

// ===== 3. ENVIAR MENSAJE DE PROGRESO AL USUARIO =====
// Usa API de Telegram directamente para no esperar respuesta
await this.helpers.httpRequest({
  method: 'POST',
  url: `https://api.telegram.org/bot${$credentials.telegramApi.accessToken}/sendMessage`,
  body: {
    chat_id: chatId,
    text: '⏳ Descargando y analizando material...'
  },
  json: true
});

// ===== 4. PREPARAR CONTEXTO PARA LA IA =====
// Formatea la información del material en texto descriptivo
const materialContext = `
Título: ${materialResponse.title}
Tipo: ${materialResponse.material_type || 'PDF'}
Curso: ${materialResponse.course?.name || 'No especificado'}
Descripción: ${materialResponse.description || 'Sin descripción'}

NOTA: Evaluación basada en metadata. 
Para evaluación completa implementar extracción de texto PDF.
`;

// ===== 5. RETORNAR DATOS PARA EL SIGUIENTE NODO =====
return {
  json: {
    chatId: chatId,
    materialId: materialId,
    materialTitle: materialResponse.title,
    materialContext: materialContext  // Esto va a la IA
  }
};
```

#### Interacción con el Backend:

**Request enviado:**
```http
GET /api/materials/abc123-def456 HTTP/1.1
Host: edurag-zpil.onrender.com
```

**Código del Backend (`materials.py`):**
```python
@router.get("/{material_id}")
async def get_material(material_id: str):
    result = supabase.table("materials") \
        .select("*, course:courses(*)") \
        .eq("id", material_id) \
        .single() \
        .execute()
    return result.data
```

**Response recibido:**
```json
{
  "id": "abc123-def456",
  "title": "Introducción a Python",
  "material_type": "lecture_notes",
  "description": "Conceptos básicos de programación",
  "file_url": "course-materials/python.pdf",
  "course": {
    "id": "course-123",
    "name": "Programación Básica"
  }
}
```

#### ¿Qué ve el usuario?
1. Envía: `/calificar abc123`
2. Recibe inmediatamente: "⏳ Descargando y analizando material..."
3. Espera mientras la IA procesa...

#### Datos de Salida:

```json
{
  "chatId": 987654321,
  "materialId": "abc123-def456",
  "materialTitle": "Introducción a Python",
  "materialContext": "Título: Introducción a Python\nTipo: lecture_notes\nCurso: Programación Básica..."
}
```

#### Siguiente Nodo:
**[7] AI Grading** recibe el contexto preparado

---

### 🤖 [7] AI Grading (OpenAI)

**Tipo de Nodo:** `n8n-nodes-base.openAi` (OpenAI Node v1)

#### ¿Qué hace?
Este es el **AGENTE DE IA** - El corazón del sistema de calificación.

- Envía el contexto del material a **OpenAI**
- Usa el modelo **gpt-4o-mini** (eficiente y económico)
- Recibe una **calificación estructurada** en JSON

#### Configuración Completa:

```javascript
{
  "resource": "text",           // Tipo: Generación de texto
  "operation": "message",       // Operación: Chat completion
  "modelId": "gpt-4o-mini",    // Modelo de IA
  
  // ===== MENSAJES =====
  "messages": {
    "messageValues": [
      {
        "role": "system",       // ← AQUÍ ESTÁ EL PROMPT DEL SISTEMA
        "content": "..."
      },
      {
        "role": "user",         // ← AQUÍ VA EL CONTEXTO DEL MATERIAL
        "content": "={{ $json.materialContext }}"
      }
    ]
  },
  
  // ===== OPCIONES =====
  "options": {
    "temperature": 0.3,   // Más determinista (0.0-2.0)
    "maxTokens": 500      // Longitud máxima de respuesta
  }
}
```

#### 🎯 PROMPT DEL SISTEMA (Instrucciones a la IA):

```text
Eres un asistente educativo experto en evaluar materiales académicos.

CRITERIOS:

1. COHERENCIA (0-10): Sentido lógico, fluidez, sin contradicciones
2. ESTRUCTURA (0-10): Organización, introducción/desarrollo/conclusión

RESPONDE SOLO CON JSON (sin markdown):
{
  "score": 8.5,
  "coherence_score": 9.0,
  "structure_score": 8.0,
  "strengths": ["punto1", "punto2", "punto3"],
  "improvements": ["mejora1", "mejora2", "mejora3"]
}
```

**¿Dónde está este prompt?**
- En el nodo **"AI Grading"**
- Campo **"System Message"** (primer mensaje)
- Se puede **editar** directamente en n8n

#### Prompt del Usuario (Contexto):

```text
Evalúa este material:

Título: Introducción a Python
Tipo: lecture_notes
Curso: Programación Básica
Descripción: Conceptos básicos de programación

NOTA: Evaluación basada en metadata.
Para evaluación completa implementar extracción de texto PDF.
```

#### Request Real a OpenAI API:

```json
{
  "model": "gpt-4o-mini",
  "messages": [
    {
      "role": "system",
      "content": "Eres un asistente educativo experto..."
    },
    {
      "role": "user",
      "content": "Evalúa este material:\n\nTítulo: Introducción a Python..."
    }
  ],
  "temperature": 0.3,
  "max_tokens": 500
}
```

#### Response de OpenAI:

```json
{
  "id": "chatcmpl-ABC123",
  "model": "gpt-4o-mini",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "{\n  \"score\": 8.5,\n  \"coherence_score\": 9.0,\n  \"structure_score\": 8.0,\n  \"strengths\": [\n    \"Título claro y descriptivo del contenido\",\n    \"Adecuado para nivel de curso básico\",\n    \"Tema fundamental para aprendizaje\"\n  ],\n  \"improvements\": [\n    \"Agregar más detalles en la descripción\",\n    \"Incluir objetivos de aprendizaje específicos\",\n    \"Especificar prerequisitos del material\"\n  ]\n}"
      }
    }
  ],
  "usage": {
    "prompt_tokens": 150,
    "completion_tokens": 120,
    "total_tokens": 270
  }
}
```

#### Datos que Extrae n8n:

```json
{
  "message": {
    "role": "assistant",
    "content": "{\"score\": 8.5, \"coherence_score\": 9.0, ...}"  // JSON como string
  }
}
```

#### Siguiente Nodo:
**[8] Process & Save** recibe la respuesta de la IA

---

### 💾 [8] Process & Save

**Tipo de Nodo:** `n8n-nodes-base.code` (Code Node v2)

#### ¿Qué hace?
Este nodo combina **3 operaciones críticas**:

1. **Parsea** la respuesta JSON de OpenAI
2. **Guarda** la evaluación en Supabase (vía backend)
3. **Formatea** el mensaje final para el usuario

#### Código Completo Explicado:

```javascript
// ===== 1. OBTENER DATOS DE NODOS ANTERIORES =====
const aiResponse = $input.first().json.message.content;  // JSON string de OpenAI
const context = $('Fetch & Prepare').first().json;       // Contexto del material
const username = $('Smart Router').first().json.username; // Quién califica

// ===== 2. PARSEAR RESPUESTA DE OPENAI =====
let evaluation;

try {
  // Limpiar posible markdown (```json ... ```)
  let clean = aiResponse.trim()
    .replace(/```json\n?/g, '')
    .replace(/```/g, '');
  
  // Parsear JSON
  evaluation = JSON.parse(clean);
  
  // ===== VALIDAR RANGOS (0-10) =====
  evaluation.score = Math.max(0, Math.min(10, evaluation.score || 5));
  evaluation.coherence_score = Math.max(0, Math.min(10, evaluation.coherence_score || 5));
  evaluation.structure_score = Math.max(0, Math.min(10, evaluation.structure_score || 5));
  
  // ===== VALIDAR ARRAYS =====
  if (!Array.isArray(evaluation.strengths)) {
    evaluation.strengths = ['Error en parseo'];
  }
  if (!Array.isArray(evaluation.improvements)) {
    evaluation.improvements = ['Revisar respuesta'];
  }
  
} catch (error) {
  console.error('Parse error:', error);
  
  // FALLBACK: Si falla el parseo, usar valores por defecto
  evaluation = {
    score: 5.0,
    coherence_score: 5.0,
    structure_score: 5.0,
    strengths: ['Error al parsear respuesta de IA'],
    improvements: ['Verificar configuración']
  };
}

// ===== 3. GUARDAR EN SUPABASE (VÍA BACKEND) =====
try {
  await this.helpers.httpRequest({
    method: 'POST',
    url: 'https://edurag-zpil.onrender.com/api/evaluations',
    body: {
      material_id: context.materialId,
      evaluated_by: username,
      score: evaluation.score,
      coherence_score: evaluation.coherence_score,
      structure_score: evaluation.structure_score,
      strengths: evaluation.strengths,
      improvements: evaluation.improvements,
      ai_model: 'gpt-4o-mini',
      ai_analysis: evaluation,
      pdf_type: 'metadata_only'
    },
    json: true
  });
} catch (saveError) {
  console.error('Error guardando:', saveError);
  // Continúa aunque falle el guardado (el usuario ve la calificación)
}

// ===== 4. FORMATEAR MENSAJE FINAL =====
const formatScore = (score) => {
  return typeof score === 'number' ? score.toFixed(1) : '0.0';
};

const getScoreEmoji = (score) => {
  if (score >= 9) return '🌟';
  if (score >= 7) return '✅';
  if (score >= 5) return '⚠️';
  return '❌';
};

const finalScore = evaluation.score;
const emoji = getScoreEmoji(finalScore);

const message = `${emoji} *Calificación Completada*\n\n` +
  `📄 *${context.materialTitle}*\n\n` +
  `📊 *CALIFICACIÓN FINAL: ${formatScore(finalScore)}/10*\n\n` +
  `*Desglose:*\n` +
  `• Coherencia: ${formatScore(evaluation.coherence_score)}/10\n` +
  `• Estructura: ${formatScore(evaluation.structure_score)}/10\n\n` +
  `💪 *Fortalezas:*\n` +
  evaluation.strengths.slice(0, 4).map((s, i) => `${i+1}. ${s}`).join('\n') + '\n\n' +
  `📈 *Mejoras:*\n` +
  evaluation.improvements.slice(0, 4).map((s, i) => `${i+1}. ${s}`).join('\n') + '\n\n' +
  `🤖 _Evaluado con IA por @${username}_`;

// ===== 5. RETORNAR PARA ENVIAR A TELEGRAM =====
return {
  json: {
    chatId: context.chatId,
    message: message
  }
};
```

#### ⚡ Cómo se Guardan los Datos en Supabase:

**Paso 1: n8n envía HTTP POST al backend**

```http
POST /api/evaluations HTTP/1.1
Host: edurag-zpil.onrender.com
Content-Type: application/json

{
  "material_id": "abc123-def456",
  "evaluated_by": "profesor_juan",
  "score": 8.5,
  "coherence_score": 9.0,
  "structure_score": 8.0,
  "strengths": ["Título claro", "Adecuado para nivel"],
  "improvements": ["Agregar objetivos", "Detallar prerequisitos"],
  "ai_model": "gpt-4o-mini",
  "ai_analysis": { /* objeto completo */ },
  "pdf_type": "metadata_only"
}
```

**Paso 2: Backend procesa (`evaluations.py`)**

```python
@router.post("/")
async def create_evaluation(evaluation: EvaluationCreate):
    supabase = get_supabase_client()
    
    # Insertar en tabla material_evaluations
    result = supabase.table("material_evaluations").insert({
        "material_id": evaluation.material_id,
        "evaluated_by": evaluation.evaluated_by,
        "score": evaluation.score,
        "coherence_score": evaluation.coherence_score,
        "structure_score": evaluation.structure_score,
        "strengths": evaluation.strengths,
        "improvements": evaluation.improvements,
        "ai_model": evaluation.ai_model,
        "ai_analysis": evaluation.ai_analysis,
        "pdf_type": evaluation.pdf_type
    }).execute()
    
    # Actualizar estado del material
    supabase.table("materials") \
        .update({"evaluation_status": "evaluated"}) \
        .eq("id", evaluation.material_id) \
        .execute()
    
    return result.data
```

**Paso 3: Supabase guarda en PostgreSQL**

**Tabla `material_evaluations`:**
```sql
INSERT INTO material_evaluations (
  id,
  material_id,
  evaluated_by,
  score,
  coherence_score,
  structure_score,
  strengths,
  improvements,
  ai_model,
  ai_analysis,
  pdf_type,
  evaluated_at,
  created_at
) VALUES (
  gen_random_uuid(),
  'abc123-def456',
  'profesor_juan',
  8.5,
  9.0,
  8.0,
  ARRAY['Título claro', 'Adecuado para nivel'],
  ARRAY['Agregar objetivos', 'Detallar prerequisitos'],
  'gpt-4o-mini',
  '{"score": 8.5, ...}'::jsonb,
  'metadata_only',
  NOW(),
  NOW()
);
```

**Tabla `materials` (update):**
```sql
UPDATE materials
SET evaluation_status = 'evaluated'
WHERE id = 'abc123-def456';
```

#### Datos de Salida:

```json
{
  "chatId": 987654321,
  "message": "✅ *Calificación Completada*\n\n📄 *Introducción a Python*\n\n📊 *CALIFICACIÓN FINAL: 8.5/10*..."
}
```

#### Siguiente Nodo:
**[9] Send to Telegram** envía el resultado al usuario

---

### 📤 [9] Send to Telegram

**Tipo de Nodo:** `n8n-nodes-base.telegram` (Telegram Node v1.2)

#### ¿Qué hace?
- **Envía el mensaje final** al usuario en Telegram
- Soporta **Markdown** para formateo (negritas, código, etc)
- Es el **punto final** de todos los flujos

#### Configuración:

```javascript
{
  "chatId": "={{ $json.chatId }}",        // A quién enviar
  "text": "={{ $json.message }}",         // Qué enviar
  "additionalFields": {
    "parse_mode": "Markdown"              // Formato del texto
  }
}
```

#### Request Real a Telegram API:

```http
POST https://api.telegram.org/bot1234567890:ABC.../sendMessage
Content-Type: application/json

{
  "chat_id": 987654321,
  "text": "✅ *Calificación Completada*\n\n📄 *Introducción a Python*...",
  "parse_mode": "Markdown"
}
```

#### ¿Qué ve el usuario en Telegram?

```
✅ Calificación Completada

📄 Introducción a Python

📊 CALIFICACIÓN FINAL: 8.5/10

Desglose:
• Coherencia: 9.0/10
• Estructura: 8.0/10

💪 Fortalezas:
1. Título claro y descriptivo
2. Adecuado para nivel de curso
3. Tema fundamental

📈 Mejoras:
1. Agregar objetivos de aprendizaje
2. Detallar prerequisitos
3. Incluir más ejemplos

🤖 Evaluado con IA por @profesor_juan
```

---

## 🚀 Desencadenamiento del Workflow

### ¿Cómo se Activa el Workflow?

#### 1. **Activación Inicial**

En n8n:
```
1. Importa n8n_workflow_optimized.json
2. Configura credenciales (Telegram + OpenAI)
3. Click en toggle "Active" (arriba a la derecha)
```

Cuando activas el workflow:
- n8n **registra un webhook** con Telegram
- Telegram empieza a **enviar** todos los mensajes del bot a n8n
- El nodo **Telegram Trigger** queda escuchando 24/7

#### 2. **Verificar Webhook Registrado**

```bash
curl https://api.telegram.org/bot{YOUR_TOKEN}/getWebhookInfo
```

Response esperado:
```json
{
  "ok": true,
  "result": {
    "url": "https://your-n8n-instance.com/webhook/telegram-xxxxx",
    "has_custom_certificate": false,
    "pending_update_count": 0,
    "max_connections": 40
  }
}
```

### Flujo de Ejecución Completo:

```
1. Usuario envía mensaje en Telegram
   ↓
2. Telegram envía webhook a n8n
   POST https://n8n.instance.com/webhook/telegram-xxxxx
   Body: { "message": { "text": "/calificar abc123", ... } }
   ↓
3. n8n recibe el webhook
   ↓
4. Telegram Trigger se activa
   ↓
5. Smart Router analiza el comando
   ↓
6. Route Command distribuye el flujo
   ↓
7. (Si es /calificar) Fetch & Prepare obtiene material
   ↓
8. AI Grading llama a OpenAI
   ↓
9. Process & Save guarda en Supabase
   ↓
10. Send to Telegram envía respuesta
    ↓
11. Usuario recibe resultado en Telegram
```

### Tiempo de Ejecución:

| Comando | Tiempo Estimado |
|---------|----------------|
| `/help` | ~1-2 segundos |
| `/pendientes` | ~2-4 segundos |
| `/calificar` | ~10-15 segundos |

---

## 🧪 Cómo Probar el Sistema

### Prerequisitos:

✅ Backend desplegado en Render  
✅ Supabase configurado con SQL migration  
✅ Bot de Telegram creado con @BotFather  
✅ n8n con workflow importado y activo  
✅ Credenciales configuradas (Telegram + OpenAI)  

---

### 🔧 Prueba 1: Comando /help

**Objetivo:** Verificar que el bot responde

#### Pasos:
1. Abre Telegram
2. Busca tu bot (ej: `@edurag_assistant_bot`)
3. Presiona **"Start"**
4. Envía: `/help`

#### Resultado Esperado:
```
🤖 EduRAG Bot - IA de Calificación

Comandos:
📋 /pendientes - Ver materiales sin calificar
🤖 /calificar [ID] - Calificar con IA
❓ /help - Esta ayuda

✨ Powered by OpenAI gpt-4o-mini
```

#### Si Falla:
- Verifica que el workflow esté **Active** en n8n
- Revisa credenciales de Telegram
- Consulta logs en n8n (Settings → Log Streaming)

---

### 📋 Prueba 2: Comando /pendientes

**Objetivo:** Verificar conexión con backend y Supabase

#### Pasos Previos:
1. Sube un PDF desde el frontend web
2. Verifica que se procesó correctamente
3. Confirma que `evaluation_status = 'pending'` en Supabase

#### Pasos de Prueba:
1. En Telegram, envía: `/pendientes`

#### Resultado Esperado:
```
📚 Materiales Pendientes

1. Introducción a Python
   📖 Programación Básica
   🆔 `abc123-def456-ghi789`

2. Estructuras de Datos
   📖 Algoritmos
   🆔 `xyz789-uvw456-rst123`

💡 Para calificar: `/calificar [ID]`
```

#### Si No Hay Materiales:
```
✅ No hay materiales pendientes de calificar.
```

#### Si Falla:
- Verifica que el backend esté desplegado en Render
- Prueba el endpoint manualmente:
  ```bash
  curl https://edurag-zpil.onrender.com/api/evaluations/pending
  ```
- Revisa tabla `materials` en Supabase
- Verifica que existe la función `get_pending_evaluations()`

---

### 🤖 Prueba 3: Calificación con IA (COMPLETA)

**Objetivo:** Probar el flujo completo end-to-end

#### Paso 1: Obtener ID del Material

Envía `/pendientes` y **copia un ID** de la lista.

Ejemplo: `abc123-def456-ghi789`

#### Paso 2: Enviar Comando de Calificación

```
/calificar abc123-def456-ghi789
```

#### Paso 3: Esperar Respuesta

**Mensaje Intermedio (1-2 segundos después):**
```
⏳ Descargando y analizando material...
```

**Mensaje Final (10-15 segundos después):**
```
✅ Calificación Completada

📄 Introducción a Python

📊 CALIFICACIÓN FINAL: 8.5/10

Desglose:
• Coherencia: 9.0/10
• Estructura: 8.0/10

💪 Fortalezas:
1. Título claro y descriptivo del contenido
2. Adecuado para el nivel del curso básico
3. Tema fundamental para el aprendizaje

📈 Mejoras:
1. Agregar más detalles en la descripción
2. Incluir objetivos de aprendizaje específicos
3. Especificar prerequisitos del material

🤖 Evaluado con IA por @profesor_juan
```

#### Paso 4: Verificar en Supabase

```sql
-- Ver evaluación guardada
SELECT * FROM material_evaluations 
WHERE material_id = 'abc123-def456-ghi789';

-- Verificar que el material cambió de estado
SELECT id, title, evaluation_status 
FROM materials 
WHERE id = 'abc123-def456-ghi789';
-- Debe mostrar: evaluation_status = 'evaluated'
```

#### Paso 5: Verificar en Dashboard Web

1. Abre https://edu-rag-pc2d.vercel.app
2. Login como profesor
3. Ve a sección **Analytics** o **Materials**
4. Deberías ver la calificación reciente

---

### 🔍 Prueba 4: Debugging en n8n

**Objetivo:** Ver datos internos del workflow

#### Pasos:
1. En n8n, abre el workflow
2. Desactiva temporalmente (`Active` → OFF)
3. Click en **"Execute Workflow"** (botón play arriba)
4. En Telegram, envía un comando
5. En n8n, verás la ejecución manual

#### Ver Output de Cada Nodo:
1. Click en un nodo ejecutado
2. Pestaña **"Output Data"**
3. Inspecciona el JSON completo

**Ejemplo: Output de Smart Router**
```json
{
  "command": "calificar",
  "chatId": 987654321,
  "materialId": "abc123-def456",
  "username": "profesor_juan"
}
```

**Ejemplo: Output de AI Grading**
```json
{
  "message": {
    "role": "assistant",
    "content": "{\"score\": 8.5, \"coherence_score\": 9.0, ...}"
  }
}
```

---

### ⚠️ Prueba 5: Manejo de Errores

**Objetivo:** Verificar que el sistema maneja errores gracefully

#### Prueba A: ID Inválido

Envía:
```
/calificar id-invalido-123
```

**Esperado:**
```
❌ Material no encontrado
```

#### Prueba B: Comando Mal Formateado

Envía:
```
/calificar
```
(Sin ID)

**Esperado:**
```
❌ Comando no reconocido. Usa `/help` para ver comandos.
```

#### Prueba C: Material Ya Calificado

1. Califica un material
2. Intenta calificarlo de nuevo con mismo ID

**Esperado:**
- Debe permitirlo (puede re-evaluar)
- Guarda nueva evaluación
- Actualiza fecha de evaluación

---

### 📊 Prueba 6: Verificar Logs

#### En n8n:

1. Settings → Log Streaming
2. Activa logs
3. Ejecuta comandos
4. Observa logs en tiempo real

#### En Render (Backend):

```bash
# Logs en tiempo real
render logs -f --service edurag-backend

# Buscar errores
render logs --service edurag-backend | grep ERROR

# Filtrar por endpoint de evaluations
render logs --service edurag-backend | grep "/api/evaluations"
```

#### En Supabase:

1. Dashboard → Database → Logs
2. Filtrar por tabla `material_evaluations`
3. Ver queries recientes

---

### 🎯 Checklist de Pruebas Completo

- [ ] Bot responde a `/help`
- [ ] Bot responde a comandos desconocidos con error
- [ ] `/pendientes` muestra lista (si hay materiales)
- [ ] `/pendientes` muestra "no hay" (si lista vacía)
- [ ] `/calificar [ID]` envía mensaje de progreso
- [ ] IA retorna calificación en 10-15 segundos
- [ ] Calificación tiene formato correcto (emojis, negritas)
- [ ] Evaluación se guarda en Supabase
- [ ] Material cambia a `evaluation_status = 'evaluated'`
- [ ] Dashboard web muestra la evaluación
- [ ] Workflow maneja IDs inválidos con error
- [ ] Logs de n8n muestran ejecuciones exitosas
- [ ] Backend logs no muestran errores 500

---

## 📚 Resumen Ejecutivo

### Nodos del Workflow:

| # | Nodo | Tipo | Función Principal |
|---|------|------|-------------------|
| 1 | Telegram Trigger | Trigger | Escucha mensajes del bot 24/7 |
| 2 | Smart Router | Code | Detecta comando + Valida + Extrae parámetros |
| 3 | Route Command | Switch | Distribuye según tipo de comando |
| 4 | Get Pending | HTTP | Obtiene lista de materiales pendientes |
| 5 | Format Response | Code | Formatea respuestas para Telegram |
| 6 | Fetch & Prepare | Code | Obtiene material + Envía progreso + Prepara contexto |
| 7 | **AI Grading** | **OpenAI** | **🤖 AGENTE DE IA - Califica el material** |
| 8 | Process & Save | Code | Parsea IA + Guarda en Supabase + Formatea |
| 9 | Send to Telegram | Telegram | Envía respuesta final al usuario |

### Prompt del Sistema:

**Ubicación:** Nodo [7] AI Grading → System Message

**Contenido:**
```
Eres un asistente educativo experto en evaluar materiales académicos.

CRITERIOS:
1. COHERENCIA (0-10)
2. ESTRUCTURA (0-10)

RESPONDE SOLO CON JSON:
{ "score": 8.5, "coherence_score": 9.0, ... }
```

### Cómo se Guardan Datos:

```
n8n [8] Process & Save
    ↓ HTTP POST
Backend /api/evaluations
    ↓ Supabase Client
Supabase PostgreSQL
    ↓ INSERT
Tabla: material_evaluations
```

### Cómo se Desencadena:

```
Usuario → Telegram → Webhook → n8n → Workflow
```

### Cómo Probar:

1. `/help` - Verifica bot activo
2. `/pendientes` - Verifica backend + DB
3. `/calificar [ID]` - Prueba completa con IA

---

**¡Sistema listo para usar!** 🎉

Para cualquier problema, revisa logs en n8n o consulta las secciones de troubleshooting.
