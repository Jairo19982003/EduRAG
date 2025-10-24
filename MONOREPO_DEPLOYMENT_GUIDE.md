# 🚀 Guía de Deployment - Monorepo (Un Solo Repositorio)

## 📌 Tu Situación Actual

Tienes un **monorepo** en GitHub con esta estructura:
```
EduRAG/
├── edurag/
│   ├── backend/      ← Desplegar en Render
│   ├── frontend/     ← Desplegar en Vercel
│   └── mcp-server/   ← Opcional (MCP local)
├── documentation/
├── docs/
└── README.md
```

**✅ NO necesitas crear repositorios separados**

Render, Vercel y Netlify soportan **monorepos** usando la configuración de **Root Directory**.

---

## 1️⃣ Backend en Render (Configuración para Monorepo)

### Paso a Paso:

1. **Ir a Render Dashboard:** https://dashboard.render.com

2. **New Web Service:**
   - Click "New +" → "Web Service"
   - Conectar tu repositorio `EduRAG` (el repositorio completo)

3. **Configuración Crítica - Root Directory:**

   ```yaml
   Name: edurag-backend
   Runtime: Python 3
   
   # ⚠️ IMPORTANTE: Especificar subdirectorio
   Root Directory: edurag/backend
   
   # Build Command:
   pip install -r requirements.txt
   
   # Start Command:
   gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
   
   # Instance Type:
   Free (o Starter $7/mes para always-on)
   ```

4. **Environment Variables:**
   ```
   SUPABASE_URL=https://tu-proyecto.supabase.co
   SUPABASE_KEY=tu_supabase_anon_key
   OPENAI_API_KEY=sk-tu-key-aqui
   PYTHON_VERSION=3.11.0
   ```

5. **Deploy:**
   - Click "Create Web Service"
   - Render detectará cambios solo en `edurag/backend/`
   - URL final: `https://edurag-backend.onrender.com`

### ⚙️ Configuración Alternativa (render.yaml)

Si prefieres configuración como código, crea `render.yaml` en la **raíz del repo**:

```yaml
# render.yaml (en la raíz del proyecto)
services:
  - type: web
    name: edurag-backend
    runtime: python
    rootDir: edurag/backend  # ← Especifica el subdirectorio
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_KEY
        sync: false
      - key: OPENAI_API_KEY
        sync: false
    plan: free
```

Luego en Render:
- "New" → "Blueprint"
- Seleccionar repositorio
- Render detectará `render.yaml` automáticamente

---

## 2️⃣ Frontend en Vercel (Configuración para Monorepo)

### Paso a Paso:

1. **Ir a Vercel Dashboard:** https://vercel.com/dashboard

2. **Import Project:**
   - Click "Add New..." → "Project"
   - Seleccionar repositorio `EduRAG`

3. **Configuración Crítica - Root Directory:**

   ```yaml
   Framework Preset: Vite
   
   # ⚠️ IMPORTANTE: Especificar subdirectorio
   Root Directory: edurag/frontend
   
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

4. **Environment Variables:**
   ```
   VITE_API_URL=https://edurag-backend.onrender.com
   ```

5. **Deploy:**
   - Click "Deploy"
   - Vercel detectará cambios solo en `edurag/frontend/`
   - URL final: `https://edurag.vercel.app`

### ⚙️ Configuración Alternativa (vercel.json)

Crear `vercel.json` en `edurag/frontend/`:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "installCommand": "npm install"
}
```

---

## 3️⃣ MCP Server - ¿Se puede desplegar?

### Respuesta: **Sí, pero con consideraciones**

El **MCP (Model Context Protocol) Server** típicamente corre **localmente** como herramienta de desarrollo, pero hay opciones:

### Opción A: MCP Local (Recomendado para desarrollo)

**Uso típico:**
- MCP server corre en tu máquina local
- Se conecta a VS Code como extensión
- No requiere deployment

**Cuándo usar:**
- Durante desarrollo
- Para asistencia de código con IA
- Herramientas de productividad personal

### Opción B: MCP como Servicio Web (Avanzado)

Si quieres que MCP sea accesible remotamente:

#### En Render:

```yaml
# render.yaml
services:
  - type: web
    name: edurag-mcp-server
    runtime: node
    rootDir: edurag/mcp-server  # ← Subdirectorio MCP
    buildCommand: npm install && npm run build
    startCommand: npm start
    envVars:
      - key: NODE_VERSION
        value: 18.0.0
      - key: MCP_PORT
        value: 3000
    plan: free
```

**Consideraciones:**
- ⚠️ MCP servers suelen ser para uso local (VSCode)
- ⚠️ Exponerlo públicamente puede tener implicaciones de seguridad
- ⚠️ Necesitarías autenticación adicional

### Opción C: No Desplegar MCP (Más Común)

**Recomendación:** Deja MCP solo para desarrollo local.

Si tu proyecto no usa activamente MCP para funcionalidad del usuario final, **no necesitas desplegarlo**.

---

## 🎯 Configuración Recomendada para Ti

### Tu Estructura de Deployment:

```
┌─────────────────────────────────────────┐
│  GitHub: github.com/usuario/EduRAG      │
│  (Un solo repositorio - monorepo)       │
└─────────────────────────────────────────┘
               │
               ├──────────────────────┬─────────────────┐
               │                      │                 │
               ▼                      ▼                 ▼
┌──────────────────────┐  ┌──────────────────┐  ┌──────────────┐
│   Render.com         │  │   Vercel.com     │  │ MCP Server   │
│   Backend API        │  │   Frontend SPA   │  │ (Local)      │
│                      │  │                  │  │              │
│ Root: edurag/backend │  │ Root: edurag/    │  │ No Deploy    │
│                      │  │       frontend   │  │              │
│ Port: 8000           │  │ Port: N/A (CDN)  │  │              │
└──────────────────────┘  └──────────────────┘  └──────────────┘
```

---

## 📝 Guía de Configuración Detallada

### Archivo: `render.yaml` (Opcional - en raíz del proyecto)

```yaml
# render.yaml
# Colocar en: Proyecto_Final/render.yaml

services:
  # Backend Service
  - type: web
    name: edurag-backend
    runtime: python
    rootDir: edurag/backend
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_KEY
        sync: false
      - key: OPENAI_API_KEY
        sync: false
    healthCheckPath: /
    plan: free
    
    # Auto-deploy cuando cambie edurag/backend/
    autoDeploy: true
```

### Archivo: `vercel.json` (Opcional - en edurag/frontend/)

```json
{
  "version": 2,
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "installCommand": "npm install",
  "routes": [
    {
      "src": "/.*",
      "dest": "/index.html"
    }
  ]
}
```

---

## 🔄 Auto-Deploy Inteligente

### Render Auto-Deploy:

Render puede detectar cambios **solo en `edurag/backend/`** y re-deployar automáticamente.

**Configuración:**
1. En Render Dashboard → Tu servicio → Settings
2. Activar "Auto-Deploy" 
3. Render detecta cambios en `edurag/backend/` vía Git hooks

### Vercel Auto-Deploy:

Similar, Vercel detecta cambios solo en `edurag/frontend/`.

**Configuración:**
1. En Vercel Dashboard → Tu proyecto → Settings
2. Git Integration → Activado por defecto
3. Vercel detecta cambios en `edurag/frontend/`

**Resultado:** ✅ Push a `edurag/backend/` → Solo backend se redeploya  
✅ Push a `edurag/frontend/` → Solo frontend se redeploya

---

## 🆚 Comparación: Monorepo vs. Repos Separados

| Aspecto | Monorepo (1 repo) | Repos Separados (3 repos) |
|---------|-------------------|---------------------------|
| **Configuración** | ✅ Root Directory en cada servicio | ⚠️ Crear 3 repos diferentes |
| **Versionado** | ✅ Todo sincronizado | ❌ Versiones pueden desincronizarse |
| **Documentación** | ✅ Un solo README | ❌ 3 READMEs que mantener |
| **Pull Requests** | ✅ Un PR para cambios fullstack | ❌ PRs en múltiples repos |
| **CI/CD** | ✅ Un solo workflow | ⚠️ 3 workflows separados |
| **Complejidad** | ✅ Baja (todo en un lugar) | ❌ Alta (sincronizar 3 repos) |
| **Deployment** | ✅ Soportado por Render/Vercel | ✅ También soportado |

**Recomendación:** ✅ **Mantén el monorepo** (un solo repositorio)

---

## 🛠️ Comandos para Verificar Configuración

### Verificar estructura del proyecto:

```powershell
cd "c:\Users\admin\Desktop\OCTAVO SEMESTRE\DESARROLLO WEB\EXAMEN FINAL\Proyecto_Final"

# Verificar que los subdirectorios existen
Test-Path edurag/backend
Test-Path edurag/frontend
Test-Path edurag/mcp-server

# Verificar archivos críticos
Test-Path edurag/backend/requirements.txt
Test-Path edurag/backend/main.py
Test-Path edurag/frontend/package.json
```

### Verificar que Git está configurado correctamente:

```powershell
# Ver repositorio remoto
git remote -v

# Debería mostrar algo como:
# origin  https://github.com/usuario/EduRAG.git (fetch)
# origin  https://github.com/usuario/EduRAG.git (push)
```

---

## 📋 Checklist de Deployment

### Backend en Render:
- [ ] Conectar repositorio en Render
- [ ] Configurar **Root Directory: `edurag/backend`**
- [ ] Verificar Build Command: `pip install -r requirements.txt`
- [ ] Verificar Start Command: `gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
- [ ] Agregar variables de entorno (SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY)
- [ ] Deploy y verificar en `/docs` (Swagger UI)

### Frontend en Vercel:
- [ ] Conectar repositorio en Vercel
- [ ] Configurar **Root Directory: `edurag/frontend`**
- [ ] Verificar Build Command: `npm run build`
- [ ] Verificar Output Directory: `dist`
- [ ] Agregar variable `VITE_API_URL` con URL del backend
- [ ] Deploy y verificar que carga correctamente

### MCP Server:
- [ ] **No desplegar** - solo uso local ✅
- [ ] (Opcional) Si necesitas acceso remoto, desplegar en Render con `rootDir: edurag/mcp-server`

---

## 🐛 Troubleshooting

### Error: "No such file or directory: requirements.txt"

**Causa:** Root Directory no configurado correctamente.

**Solución:**
```yaml
Root Directory: edurag/backend  # ← Asegúrate de tener esto
```

### Error: "Build failed - Cannot find package.json"

**Causa:** Root Directory apunta a lugar incorrecto.

**Solución en Vercel:**
```yaml
Root Directory: edurag/frontend  # ← Debe apuntar aquí
```

### Error: "Port already in use"

**Causa:** Start command usa puerto fijo en lugar de variable.

**Solución:**
```bash
# ❌ Incorrecto:
gunicorn main:app --bind 0.0.0.0:8000

# ✅ Correcto (usa variable $PORT de Render):
gunicorn main:app --bind 0.0.0.0:$PORT
```

### Backend deploy exitoso pero frontend no conecta

**Causa:** CORS no configurado o URL incorrecta.

**Solución 1 - CORS en backend:**
```python
# edurag/backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://edurag.vercel.app",  # ← Agregar tu URL de Vercel
        "https://*.vercel.app",       # ← Permite previews
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Solución 2 - Variable de entorno en Vercel:**
```
VITE_API_URL=https://edurag-backend.onrender.com
```

---

## 🎯 Resumen de Respuestas

### 1. ¿Cómo desplegar solo backend si todo está en un repo?

**Respuesta:** Usa la configuración **Root Directory** en Render:
- Root Directory: `edurag/backend`
- Render solo mira ese subdirectorio

### 2. ¿Crear repos separados?

**Respuesta:** **NO**. Los monorepos son soportados y preferibles:
- ✅ Mantén todo en un repositorio
- ✅ Usa Root Directory para separar servicios
- ✅ Más fácil de mantener

### 3. ¿Se puede desplegar MCP Server?

**Respuesta:** **Sí, pero no es necesario**:
- MCP típicamente es para desarrollo local (VS Code)
- **Recomendación:** No desplegar MCP
- Si necesitas: Usar Root Directory: `edurag/mcp-server` en Render

---

## 📖 Recursos Adicionales

- **Render Monorepo Docs:** https://render.com/docs/monorepo-support
- **Vercel Monorepo Docs:** https://vercel.com/docs/concepts/git/monorepos
- **GitHub Monorepo Best Practices:** https://github.blog/2021-11-10-make-your-monorepo-feel-small-with-gits-sparse-index/

---

**¿Necesitas ayuda con la configuración específica?** ¡Avísame y te ayudo paso a paso! 🚀
