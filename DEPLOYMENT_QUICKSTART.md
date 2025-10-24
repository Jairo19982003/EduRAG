# 🚀 Deployment Rápido - Monorepo EduRAG

## TL;DR - Respuestas Rápidas

### ❓ ¿Necesito crear repos separados?
**NO** ❌ - Render y Vercel soportan monorepos perfectamente.

### ❓ ¿Cómo desplegar solo backend?
**Usa Root Directory: `edurag/backend`** en Render.

### ❓ ¿Puedo desplegar MCP Server?
**Sí, pero NO es necesario** - MCP es para desarrollo local.

---

## 🎯 Configuración en 3 Pasos

### 1️⃣ Backend en Render

```yaml
Root Directory: edurag/backend
Build Command: pip install -r requirements.txt
Start Command: gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT

Variables de Entorno:
- SUPABASE_URL
- SUPABASE_KEY
- OPENAI_API_KEY
```

**URL resultante:** `https://edurag-backend.onrender.com`

---

### 2️⃣ Frontend en Vercel

```yaml
Root Directory: edurag/frontend
Build Command: npm run build
Output Directory: dist

Variables de Entorno:
- VITE_API_URL=https://edurag-backend.onrender.com
```

**URL resultante:** `https://edurag.vercel.app`

---

### 3️⃣ MCP Server

**Opción Recomendada:** ❌ No desplegar - Solo local para desarrollo

**Opción Avanzada:** Si necesitas acceso remoto:
```yaml
Root Directory: edurag/mcp-server
Build Command: npm install && npm run build
Start Command: npm start
```

---

## 📊 Diagrama Visual

```
┌──────────────────────────────────────────┐
│     GitHub Repo: EduRAG (Monorepo)       │
│  https://github.com/usuario/EduRAG       │
└──────────────────┬───────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│  Render  │ │  Vercel  │ │   MCP    │
│ Backend  │ │ Frontend │ │  Local   │
├──────────┤ ├──────────┤ └──────────┘
│ Root:    │ │ Root:    │
│ edurag/  │ │ edurag/  │
│ backend  │ │ frontend │
└──────────┘ └──────────┘
```

---

## ✅ Pasos Específicos

### Render (Backend)

1. Ve a: https://dashboard.render.com
2. Click: "New +" → "Web Service"
3. Conecta: Repositorio `EduRAG`
4. **Configura:**
   - Name: `edurag-backend`
   - Runtime: `Python 3`
   - **Root Directory:** `edurag/backend` ⚠️
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
5. **Variables de Entorno:** Agregar SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY
6. Click: "Create Web Service"

### Vercel (Frontend)

1. Ve a: https://vercel.com/dashboard
2. Click: "Add New..." → "Project"
3. Conecta: Repositorio `EduRAG`
4. **Configura:**
   - Framework: `Vite`
   - **Root Directory:** `edurag/frontend` ⚠️
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. **Variables de Entorno:** Agregar `VITE_API_URL` con URL del backend
6. Click: "Deploy"

---

## 🔧 Archivos de Configuración Creados

Ya he creado estos archivos para ti:

1. ✅ **`render.yaml`** (raíz del proyecto)
   - Configuración automática para Render
   - Uso: "New" → "Blueprint" en Render

2. ✅ **`edurag/frontend/vercel.json`**
   - Configuración para Vercel
   - Detectado automáticamente

3. ✅ **`MONOREPO_DEPLOYMENT_GUIDE.md`**
   - Guía completa con troubleshooting

---

## 🐛 Errores Comunes

### ❌ "No such file: requirements.txt"
**Solución:** Verifica que Root Directory sea `edurag/backend`

### ❌ "Cannot find package.json"
**Solución:** Verifica que Root Directory sea `edurag/frontend`

### ❌ "CORS error" en frontend
**Solución:** Agrega tu URL de Vercel en CORS del backend:
```python
allow_origins=[
    "https://edurag.vercel.app",
    "https://*.vercel.app",
]
```

---

## 📝 Commit y Push

Si hiciste cambios (agregaste render.yaml, vercel.json):

```powershell
cd "c:\Users\admin\Desktop\OCTAVO SEMESTRE\DESARROLLO WEB\EXAMEN FINAL\Proyecto_Final"

git add render.yaml edurag/frontend/vercel.json
git commit -m "Add deployment configuration for Render and Vercel"
git push origin master
```

---

## 🎯 Siguiente Paso

1. **Ve a `MONOREPO_DEPLOYMENT_GUIDE.md`** para guía completa
2. **Usa `render.yaml`** para deployment automático en Render
3. **Sigue la configuración de Root Directory** en ambos servicios

¡Listo para deployar! 🚀
