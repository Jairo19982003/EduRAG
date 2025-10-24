# 🚀 Guía Rápida: Subir a GitHub y Deployar

## ✅ Resumen de lo Completado

### 1. `.gitignore` Creado ✅
- Excluye `node_modules/` (frontend y mcp-server)
- Excluye `__pycache__/`, `*.pyc` (Python)
- Excluye `.env` (archivos de entorno)
- Excluye `venv/`, `env/` (entornos virtuales Python)
- Excluye archivos de sistema (`.DS_Store`, `Thumbs.db`)
- Excluye builds (`dist/`, `build/`)
- Excluye IDE configs (`.vscode/`, `.idea/`)

### 2. `.env.example` Creado ✅
- Plantilla de variables de entorno
- Sin credenciales reales (seguro para Git)

### 3. Documentación de Deployment ✅
- `DEPLOYMENT_GUIDE.md` con 5 opciones completas
- Guías paso a paso para cada opción
- Comparación de costos y dificultad

---

## 📋 Pasos para Subir a GitHub

### Paso 1: Limpiar Archivos .env de Git

⚠️ **IMPORTANTE:** Los archivos `.env` están actualmente rastreados por Git. Debemos removerlos:

```powershell
# Navegar al directorio del proyecto
cd "c:\Users\admin\Desktop\OCTAVO SEMESTRE\DESARROLLO WEB\EXAMEN FINAL\Proyecto_Final"

# Remover archivos .env del tracking de Git (pero NO del disco)
git rm --cached edurag/.env
git rm --cached edurag/backend/.env
git rm --cached edurag/frontend/.env
git rm --cached edurag/mcp-server/.env

# Verificar que ya no están rastreados
git status
```

### Paso 2: Hacer Commit Inicial

```powershell
# Agregar todos los archivos (excepto los del .gitignore)
git add .

# Crear commit inicial
git commit -m "Initial commit: EduRAG complete system with RAG intelligence

- Complete backend with FastAPI + RAG engine
- Complete frontend with Vue 3 + Tailwind
- Full academic documentation (9 documents, 6300+ lines)
- Full technical documentation (6 documents, 5100+ lines)
- Deployment guides for Vercel/Render/Supabase
- .gitignore configured for Python/Node/Vue
- Ready for production deployment"

# Verificar el commit
git log --oneline
```

### Paso 3: Crear Repositorio en GitHub

1. **Ir a GitHub:** https://github.com/new

2. **Configurar repositorio:**
   - **Repository name:** `EduRAG` (o tu nombre preferido)
   - **Description:** `Sistema de Gestión Educativa con RAG - FastAPI + Vue 3 + PostgreSQL + OpenAI`
   - **Visibility:** 
     - ✅ **Public** (recomendado para portafolio)
     - ⬜ Private (si prefieres privado)
   - **NO inicialices con:**
     - ❌ README (ya tienes uno)
     - ❌ .gitignore (ya tienes uno)
     - ❌ License (puedes agregar después)

3. **Click "Create repository"**

### Paso 4: Conectar con GitHub

GitHub te mostrará comandos. Si no, usa estos:

```powershell
# Verificar remotes actuales
git remote -v

# Si existe 'origin', removerlo
git remote remove origin

# Agregar nuevo remote (REEMPLAZA con TU URL de GitHub)
git remote add origin https://github.com/TU-USUARIO/EduRAG.git

# Verificar que se agregó correctamente
git remote -v
```

### Paso 5: Subir Código a GitHub

```powershell
# Verificar rama actual
git branch

# Si no estás en 'main', renombrar rama
git branch -M main

# Push inicial (la primera vez)
git push -u origin main
```

Si pide credenciales:
- **Username:** Tu username de GitHub
- **Password:** **NO uses tu password**, usa un **Personal Access Token**
  - Crear token: https://github.com/settings/tokens
  - Scopes necesarios: `repo` (full control)

---

## 🌐 Pasos para Deployar (Opción Recomendada)

### Arquitectura de Deployment:

```
Frontend (Vercel) ←→ Backend (Render) ←→ Database (Supabase)
     FREE              FREE/7$              FREE
```

---

### A. Deploy Frontend en Vercel

1. **Ir a Vercel:** https://vercel.com

2. **Login con GitHub**

3. **Import Project:**
   - Click "Add New..." → "Project"
   - Seleccionar repositorio `EduRAG`
   - Click "Import"

4. **Configurar Build Settings:**
   ```
   Framework Preset: Vite
   Root Directory: edurag/frontend
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

5. **Environment Variables:**
   ```
   VITE_API_URL = (dejarlo vacío por ahora, configurar después)
   ```

6. **Deploy:**
   - Click "Deploy"
   - Esperar 2-3 minutos
   - Obtendrás URL como: `https://edurag-xxx.vercel.app`

---

### B. Deploy Backend en Render

1. **Ir a Render:** https://render.com

2. **Login con GitHub**

3. **New Web Service:**
   - Click "New +" → "Web Service"
   - Conectar repositorio `EduRAG`

4. **Configurar:**
   ```
   Name: edurag-backend
   Runtime: Python 3
   Root Directory: edurag/backend
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

5. **Agregar a `edurag/backend/requirements.txt`** (si no está):
   ```
   gunicorn==21.2.0
   ```
   Luego commit y push:
   ```powershell
   git add edurag/backend/requirements.txt
   git commit -m "Add gunicorn for production"
   git push
   ```

6. **Environment Variables en Render:**
   ```
   SUPABASE_URL = https://tu-proyecto.supabase.co
   SUPABASE_KEY = tu_supabase_anon_key
   OPENAI_API_KEY = sk-tu-key-aqui
   ```

7. **Deploy:**
   - Click "Create Web Service"
   - Esperar 5-10 minutos
   - Obtendrás URL como: `https://edurag-backend.onrender.com`

---

### C. Actualizar URLs

1. **Backend → Permitir Frontend:**

   Editar `edurag/backend/main.py`:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "http://localhost:5173",
           "https://edurag-xxx.vercel.app",  # ← TU URL DE VERCEL
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

   Commit y push:
   ```powershell
   git add edurag/backend/main.py
   git commit -m "Update CORS for production"
   git push
   ```

2. **Frontend → Apuntar a Backend:**

   En Vercel Dashboard:
   - Settings → Environment Variables
   - Editar `VITE_API_URL`:
     ```
     VITE_API_URL = https://edurag-backend.onrender.com
     ```
   - Click "Save"
   - Re-deploy automático

---

### D. Verificar Deployment ✅

1. **Frontend:** Ir a `https://edurag-xxx.vercel.app`
   - Debería cargar la interfaz
   - Verificar que no hay errores en consola (F12)

2. **Backend:** Ir a `https://edurag-backend.onrender.com/docs`
   - Debería mostrar Swagger UI
   - Probar endpoint de health check

3. **Integración:**
   - Login en frontend
   - Crear un estudiante
   - Verificar que se crea correctamente

---

## 📊 Checklist Final

### Antes de Subir a GitHub:
- [x] `.gitignore` creado y completo
- [ ] Archivos `.env` removidos del tracking de Git
- [ ] `.env.example` creado con variables de ejemplo
- [ ] README.md actualizado
- [ ] Documentación completa en carpetas `docs/` y `documentation/`
- [ ] Commit inicial creado

### Antes de Deployar:
- [ ] Repositorio en GitHub creado y código subido
- [ ] `gunicorn` agregado a `requirements.txt`
- [ ] Variables de entorno de Supabase y OpenAI disponibles
- [ ] CORS configurado en backend con URL de producción

### Post-Deployment:
- [ ] Frontend accesible y sin errores
- [ ] Backend API funcionando (Swagger UI)
- [ ] Base de datos conectada
- [ ] Chat RAG funcionando correctamente
- [ ] URLs actualizadas en ambos servicios

---

## 🆘 Solución de Problemas Comunes

### Error: "git: '.env' is tracked"

```powershell
# Remover del tracking pero mantener en disco
git rm --cached edurag/backend/.env
git commit -m "Remove .env from tracking"
```

### Error: "CORS policy blocking request"

- Verificar que URL de frontend esté en `allow_origins` del backend
- Verificar que CORS middleware esté antes de los routers
- Re-deploy backend después de cambiar CORS

### Error: "Module not found" en Render

- Verificar que `requirements.txt` tenga todas las dependencias
- Verificar que `Root Directory` sea `edurag/backend`
- Verificar logs de build en Render dashboard

### Error: "Cannot connect to database"

- Verificar que variables `SUPABASE_URL` y `SUPABASE_KEY` estén configuradas en Render
- Verificar que las credenciales sean correctas
- Verificar que pgvector extension esté activada en Supabase

---

## 💰 Costos Estimados

| Servicio | Plan | Costo |
|----------|------|-------|
| Vercel (Frontend) | Hobby (Free) | $0/mes |
| Render (Backend) | Free (750h) | $0/mes* |
| Supabase (DB) | Free | $0/mes |
| OpenAI API | Pay-as-you-go | $5-15/mes |
| **TOTAL** | | **$5-15/mes** |

*Nota: Render Free plan hace "sleep" después de 15min de inactividad (cold start de ~30s). Para always-on: $7/mes.

---

## 📞 Recursos Útiles

- **Vercel Docs:** https://vercel.com/docs
- **Render Docs:** https://render.com/docs
- **Supabase Docs:** https://supabase.com/docs
- **FastAPI Deployment:** https://fastapi.tiangolo.com/deployment/
- **Vue Production:** https://vuejs.org/guide/best-practices/production-deployment.html

---

## ✅ Comando Único para GitHub (Después de limpiar .env)

```powershell
# Todo en uno (después de remover .env del tracking)
cd "c:\Users\admin\Desktop\OCTAVO SEMESTRE\DESARROLLO WEB\EXAMEN FINAL\Proyecto_Final"
git add .
git commit -m "Initial commit: EduRAG complete system"
git remote add origin https://github.com/TU-USUARIO/EduRAG.git
git push -u origin main
```

¡Listo! 🎉
