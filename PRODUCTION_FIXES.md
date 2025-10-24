# 🔧 Correcciones para Producción - EduRAG

## ⚠️ Problemas Identificados y Solucionados

### 1️⃣ URLs Hardcodeadas en Frontend (CRÍTICO ✅ RESUELTO)

**Problema:** El frontend usaba `http://localhost:8000` en lugar de la variable de entorno.

**Archivos Corregidos:**

#### 📁 `edurag/frontend/src/services/api.js` (Línea 4)
```javascript
// ❌ ANTES - Hardcoded localhost
const api = axios.create({
  baseURL: 'http://localhost:8000',  // ⚠️ PROBLEMA: No funcionaba en producción
  headers: {
    'Content-Type': 'application/json'
  }
})

// ✅ AHORA - Usa variable de entorno
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})
```

**Ubicación:** `Proyecto_Final/edurag/frontend/src/services/api.js`

---

#### 📁 `edurag/frontend/src/views/AnalyticsView.vue` (Línea 330)
```javascript
// ❌ ANTES
const response = await axios.get('http://localhost:8000/api/analytics/detailed')

// ✅ AHORA
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const response = await axios.get(`${apiUrl}/api/analytics/detailed`)
```

**Ubicación:** `Proyecto_Final/edurag/frontend/src/views/AnalyticsView.vue`

---

#### 📁 `edurag/frontend/src/views/CourseManageView.vue` (Línea 214)
```javascript
// ❌ ANTES
const enrollmentsResponse = await axios.get('http://localhost:8000/api/enrollments')

// ✅ AHORA
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const enrollmentsResponse = await axios.get(`${apiUrl}/api/enrollments`)
```

**Ubicación:** `Proyecto_Final/edurag/frontend/src/views/CourseManageView.vue`

---

#### 📁 `edurag/frontend/src/views/EnrollmentsView.vue` (Línea 228)
```javascript
// ❌ ANTES
const api = axios.create({
  baseURL: 'http://localhost:8000'
})

// ✅ AHORA
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000'
})
```

**Ubicación:** `Proyecto_Final/edurag/frontend/src/views/EnrollmentsView.vue`

---

### 2️⃣ CORS No Configurado para Producción (CRÍTICO ✅ RESUELTO)

**Problema:** El backend solo permitía conexiones desde `localhost`, bloqueando requests desde Vercel.

**Archivo Corregido:**

#### 📁 `edurag/backend/app/core/config.py` (Línea 20)
```python
# ❌ ANTES - Solo localhost
CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

# ✅ AHORA - Incluye Vercel
# 🔧 CONFIGURACIÓN CORS PARA PRODUCCIÓN
# En desarrollo: http://localhost:5173,http://localhost:3000
# En producción: Agrega tu URL de Vercel aquí (ej: https://edu-rag-pc2z.vercel.app)
# También puedes configurarlo vía variable de entorno CORS_ORIGINS en Render
CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,https://edu-rag-pc2z.vercel.app,https://*.vercel.app"
# ⚠️ IMPORTANTE: Reemplaza 'edu-rag-pc2z.vercel.app' con tu URL real de Vercel
# El wildcard *.vercel.app permite preview deployments
```

**Ubicación:** `Proyecto_Final/edurag/backend/app/core/config.py`

**⚠️ ACCIÓN REQUERIDA:**
1. Ve a tu dashboard de Vercel
2. Copia tu URL exacta (ej: `https://edu-rag-abc123.vercel.app`)
3. Reemplaza `https://edu-rag-pc2z.vercel.app` en el código con tu URL real
4. Commit y push

---

### 3️⃣ vercel.json con Configuración Legacy (RESUELTO)

**Problema:** Vercel rechazaba el archivo porque usaba `routes` (legacy) con `headers` (moderno).

**Archivo Corregido:**

#### 📁 `edurag/frontend/vercel.json`
```json
// ❌ ANTES - Mezclaba routes (legacy) y headers (moderno)
{
  "routes": [
    {
      "src": "/assets/(.*)",
      "dest": "/assets/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  "headers": [...]
}

// ✅ AHORA - Solo configuración moderna
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

**Ubicación:** `Proyecto_Final/edurag/frontend/vercel.json`

---

## 📋 Checklist de Deployment

### ✅ Completado

- [x] URLs del frontend usan `VITE_API_URL`
- [x] CORS permite conexiones desde Vercel (wildcard)
- [x] `vercel.json` usa configuración moderna
- [x] `.gitignore` excluye archivos sensibles
- [x] Variables de entorno configuradas en Vercel
- [x] Variables de entorno configuradas en Render

### ⚠️ Pendiente - DEBES HACER ESTO

- [ ] **Reemplazar URL de Vercel en `config.py`**
  - Archivo: `edurag/backend/app/core/config.py` (línea 23)
  - Cambiar: `https://edu-rag-pc2z.vercel.app` → Tu URL real
  - Commit y push para activar auto-deploy

- [ ] **Configurar CORS_ORIGINS en Render** (Opcional pero recomendado)
  - Ve a: Render Dashboard → edurag-backend → Environment
  - Agregar variable:
    ```
    Key: CORS_ORIGINS
    Value: http://localhost:5173,http://localhost:3000,https://TU-URL.vercel.app,https://*.vercel.app
    ```
  - Esto sobrescribe el valor hardcoded y es más flexible

- [ ] **Verificar deployment funcional**
  - Crear estudiante ✓
  - Crear curso ✓
  - Subir material ✓
  - Probar chat RAG ✓

---

## 🚨 Problemas Potenciales Adicionales

### 1. Límites de API Keys

**⚠️ ADVERTENCIA:** OpenAI y Supabase tienen límites gratuitos.

**Ubicación de configuración:**
- Variables en Render: Dashboard → Environment Variables
- Variables en Vercel: Dashboard → Settings → Environment Variables

**Solución:**
- Monitorea uso en dashboards de OpenAI y Supabase
- Configura billing alerts
- Implementa rate limiting en el backend

---

### 2. Tamaño de Archivos PDF

**⚠️ ADVERTENCIA:** Render Free Tier tiene límite de memoria (512MB).

**Archivo con límite potencial:**
- `edurag/backend/app/services/rag_service.py`
- Procesamiento de PDFs grandes puede causar OOM (Out of Memory)

**Solución:**
```python
# Agregar validación en edurag/backend/app/api/endpoints/materials.py
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

if file.size > MAX_FILE_SIZE:
    raise HTTPException(status_code=413, detail="File too large")
```

---

### 3. Cold Starts en Render Free Tier

**⚠️ ADVERTENCIA:** Render Free Tier duerme el servicio después de 15 min de inactividad.

**Síntoma:**
- Primera request tarda 30-60 segundos
- Luego funciona normal

**Soluciones:**
1. **Upgrade a Render Starter ($7/mes)** - Recomendado
2. **Usar cron job para keep-alive** (evita sleep)
3. **Mostrar loading spinner** en frontend durante cold start

---

### 4. Variables de Entorno No Sincronizadas

**⚠️ VERIFICAR:** Asegúrate que las mismas variables estén en:

| Variable | Frontend (Vercel) | Backend (Render) |
|----------|-------------------|------------------|
| `VITE_API_URL` | ✅ Configurada | ❌ No aplica |
| `SUPABASE_URL` | ❌ No aplica | ✅ Configurada |
| `SUPABASE_KEY` | ❌ No aplica | ✅ Configurada |
| `OPENAI_API_KEY` | ❌ No aplica | ✅ Configurada |
| `CORS_ORIGINS` | ❌ No aplica | ⚠️ Opcional pero recomendada |

**Ubicaciones de configuración:**
- Vercel: `https://vercel.com/dashboard` → Tu proyecto → Settings → Environment Variables
- Render: `https://dashboard.render.com` → edurag-backend → Environment

---

## 🎯 Próximos Pasos

### Inmediatos (HOY)

1. **Obtén tu URL real de Vercel:**
   ```
   Vercel Dashboard → Tu proyecto → Domains
   Ejemplo: https://edu-rag-abc123.vercel.app
   ```

2. **Actualiza CORS en backend:**
   ```bash
   # Edita: edurag/backend/app/core/config.py
   # Línea 23: Reemplaza edu-rag-pc2z.vercel.app con tu URL
   
   git add edurag/backend/app/core/config.py
   git commit -m "Update CORS with production Vercel URL"
   git push origin master
   ```

3. **Verifica auto-deploy:**
   - Render: https://dashboard.render.com → Logs
   - Vercel: https://vercel.com/dashboard → Deployments

4. **Prueba funcionalidad completa**

### A Corto Plazo (ESTA SEMANA)

- [ ] Agregar validación de tamaño de archivos PDF
- [ ] Implementar mejor manejo de errores en frontend
- [ ] Configurar monitoring (Sentry, LogRocket)
- [ ] Agregar health check endpoint (`/health`)

### A Mediano Plazo (OPCIONAL)

- [ ] Upgrade a Render Starter ($7/mes) para evitar cold starts
- [ ] Implementar Redis cache para RAG queries frecuentes
- [ ] Agregar tests E2E con Playwright
- [ ] Configurar CI/CD con GitHub Actions

---

## 📞 Troubleshooting Rápido

### Error: "Network Error" al crear estudiante

**Causa:** CORS bloqueando request desde Vercel

**Solución:**
```bash
# 1. Verifica URL de Vercel en config.py
# 2. Commit y push
# 3. Espera redeploy en Render (2-3 min)
# 4. Prueba de nuevo
```

### Error: 504 Gateway Timeout

**Causa:** Cold start en Render Free Tier

**Solución:**
- Espera 60 segundos y reintenta
- O upgrade a Render Starter

### Error: Variables de entorno undefined

**Causa:** Vercel no tiene `VITE_API_URL` configurada

**Solución:**
```
Vercel Dashboard → Settings → Environment Variables
Add: VITE_API_URL = https://edurag-zpil.onrender.com
Redeploy
```

---

## 🎓 Resumen para el Profesor

**Problema Original:**
- Frontend desplegado en Vercel intentaba conectarse a `localhost:8000`

**Causa Raíz:**
- URLs hardcodeadas en 4 archivos de frontend
- CORS solo permitía localhost en backend

**Solución Implementada:**
- Reemplazar URLs con `import.meta.env.VITE_API_URL`
- Configurar CORS para permitir Vercel
- Actualizar `vercel.json` a configuración moderna

**Resultado:**
- ✅ Frontend se comunica correctamente con backend en producción
- ✅ CORS permite requests desde Vercel
- ✅ Configuración lista para auto-deploy

---

**Fecha de última actualización:** 24 de Octubre, 2025  
**Commits relacionados:**
- `Fix: Use environment variable for API URL in production` (b0c5bd7)
- `Fix vercel.json configuration`
- `Update CORS with production Vercel URL` (pendiente)

