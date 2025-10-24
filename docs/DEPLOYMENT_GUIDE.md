# 🚀 Guía de Despliegue - EduRAG

## 📋 Contenido

1. [Entornos](#entornos)
2. [Despliegue Local](#despliegue-local)
3. [Despliegue en Producción](#despliegue-en-producción)
4. [Monitoreo](#monitoreo)
5. [Troubleshooting](#troubleshooting)

---

## 🌍 Entornos

### Desarrollo (Local)

**Características:**
- Backend: uvicorn con `--reload`
- Frontend: Vite dev server con HMR
- Base de datos: Supabase free tier
- Logging: nivel DEBUG
- CORS: `localhost:5173`

### Producción

**Características:**
- Backend: Gunicorn + Uvicorn workers
- Frontend: Build estático servido por Nginx
- Base de datos: Supabase Pro
- Logging: nivel INFO
- CORS: dominio específico
- HTTPS: Certificado SSL

---

## 💻 Despliegue Local

### Prerequisitos

```bash
# Python 3.11+
python --version

# Node.js 18+
node --version

# Git
git --version
```

### 1. Clonar Repositorio

```bash
git clone <repository-url>
cd Proyecto_Final
```

### 2. Backend Setup

```bash
cd edurag/backend

# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate

# Activar entorno (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env
cp .env.example .env

# Editar .env con tus credenciales
# SUPABASE_URL=https://xxxxx.supabase.co
# SUPABASE_KEY=eyJhbGc...
# OPENAI_API_KEY=sk-proj-...
```

### 3. Base de Datos Setup

```bash
# Conectarse a Supabase Dashboard
# https://app.supabase.com

# SQL Editor → Ejecutar scripts en orden:
# 1. backend/sql/create_tables.sql
# 2. backend/sql/create_vector_search_function.sql

# Habilitar pgvector en Supabase:
# Database → Extensions → Buscar "vector" → Enable
```

### 4. Frontend Setup

```bash
cd edurag/frontend

# Instalar dependencias
npm install

# Configurar API URL (opcional, ya está configurado para localhost:8000)
# src/services/api.js → baseURL: 'http://localhost:8000/api'
```

### 5. Iniciar Aplicación

**Terminal 1 - Backend:**

```bash
cd edurag/backend
python main.py

# Output esperado:
# INFO:     Started server process
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Frontend:**

```bash
cd edurag/frontend
npm run dev

# Output esperado:
# VITE v5.0.0  ready in 234 ms
#
# ➜  Local:   http://localhost:5173/
# ➜  Network: http://192.168.1.10:5173/
```

### 6. Verificar Instalación

1. Backend health: http://localhost:8000/
2. API docs: http://localhost:8000/docs
3. Frontend: http://localhost:5173/

---

## 🌐 Despliegue en Producción

### Opción 1: Render.com (Recomendado - Fácil)

#### Backend en Render

**render.yaml:**

```yaml
services:
  - type: web
    name: edurag-backend
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
    envVars:
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_KEY
        sync: false
      - key: OPENAI_API_KEY
        sync: false
      - key: PYTHON_VERSION
        value: 3.11.0
```

**Pasos:**

1. Crear cuenta en render.com
2. New Web Service → Connect Git repo
3. Configurar environment variables
4. Deploy

#### Frontend en Render

**render.yaml:**

```yaml
services:
  - type: web
    name: edurag-frontend
    runtime: node
    buildCommand: npm install && npm run build
    startCommand: npx serve -s dist -l 5173
    envVars:
      - key: NODE_VERSION
        value: 18.0.0
```

**Actualizar API URL:**

```javascript
// src/services/api.js
const apiClient = axios.create({
  baseURL: 'https://edurag-backend.onrender.com/api',  // URL de Render
  // ...
});
```

### Opción 2: Railway (Alternativa)

**railway.json:**

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Opción 3: VPS Tradicional (Ubuntu)

#### 1. Configurar Servidor

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install python3.11 python3-pip nginx git -y

# Instalar Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y
```

#### 2. Clonar y Configurar

```bash
# Clonar repositorio
cd /var/www
sudo git clone <repo-url> edurag
cd edurag

# Backend setup
cd edurag/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Crear .env con variables de producción
sudo nano .env

# Frontend build
cd ../frontend
npm install
npm run build
```

#### 3. Configurar Gunicorn

**edurag.service:**

```ini
[Unit]
Description=EduRAG Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/edurag/backend
Environment="PATH=/var/www/edurag/backend/venv/bin"
ExecStart=/var/www/edurag/backend/venv/bin/gunicorn \
    -w 4 \
    -k uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    main:app

Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Habilitar servicio
sudo cp edurag.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable edurag
sudo systemctl start edurag
```

#### 4. Configurar Nginx

**/etc/nginx/sites-available/edurag:**

```nginx
# Backend
server {
    listen 80;
    server_name api.edurag.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Frontend
server {
    listen 80;
    server_name edurag.com www.edurag.com;
    root /var/www/edurag/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/edurag /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 5. Configurar HTTPS con Let's Encrypt

```bash
# Instalar certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtener certificados
sudo certbot --nginx -d edurag.com -d www.edurag.com -d api.edurag.com

# Auto-renovación (ya configurado)
sudo systemctl status certbot.timer
```

---

## 📊 Monitoreo

### Logs del Backend

```bash
# Ver logs en tiempo real
journalctl -u edurag -f

# Logs de las últimas 100 líneas
journalctl -u edurag -n 100

# Logs del día actual
journalctl -u edurag --since today
```

### Logs del Frontend (Nginx)

```bash
# Access logs
sudo tail -f /var/log/nginx/access.log

# Error logs
sudo tail -f /var/log/nginx/error.log
```

### Monitoreo de Recursos

```bash
# CPU y memoria
htop

# Espacio en disco
df -h

# Conexiones activas
ss -tuln | grep 8000
```

### Health Checks

**Backend:**

```bash
curl http://localhost:8000/
# {"name":"EduRAG API","version":"1.0.0","status":"running"}

curl http://localhost:8000/api/rag/health
# {"status":"healthy","chunks_count":51,...}
```

**Frontend:**

```bash
curl -I http://localhost:5173/
# HTTP/1.1 200 OK
```

### Monitoreo con Uptime Robot (Externo)

1. Crear cuenta en uptimerobot.com
2. New Monitor → HTTP(s)
3. URL: https://edurag.com
4. Interval: 5 minutes
5. Alert contacts: Email

---

## 🐛 Troubleshooting

### Backend no inicia

**Error: `ModuleNotFoundError: No module named 'fastapi'`**

```bash
# Verificar que venv esté activado
which python  # Debe apuntar a venv/bin/python

# Reinstalar dependencias
pip install -r requirements.txt
```

**Error: `Missing environment variable: SUPABASE_URL`**

```bash
# Verificar .env
cat .env

# Asegurarse que existe y tiene las variables
# SUPABASE_URL=...
# SUPABASE_KEY=...
# OPENAI_API_KEY=...
```

### Frontend no conecta con Backend

**Error: `Network Error` o `CORS policy`**

```bash
# 1. Verificar que backend esté corriendo
curl http://localhost:8000/

# 2. Verificar CORS en backend (main.py)
# allow_origins debe incluir http://localhost:5173

# 3. Verificar URL en frontend (api.js)
# baseURL: 'http://localhost:8000/api'
```

### RAG retorna respuestas vacías

**Error: "No encontré información relevante"**

```bash
# 1. Verificar que material está procesado
curl http://localhost:8000/api/materials/

# Debe tener processing_status="completed" y chunks_count > 0

# 2. Verificar embeddings en DB
# Supabase Dashboard → Table Editor → material_chunks
# Verificar que embedding no sea NULL

# 3. Probar con threshold más bajo
# En rag_vector.py, cambiar match_threshold de 0.3 a 0.1
```

### PDF no se procesa

**Error: Material queda en "processing" forever**

```bash
# 1. Ver logs del backend
journalctl -u edurag -n 100 | grep "PDF processing"

# 2. Errores comunes:
# - "PDF has insufficient text" → PDF escaneado sin OCR
# - "Rate limit exceeded" → Límite de OpenAI alcanzado
# - "Supabase error" → Problema de conexión a DB

# 3. Reprocessar manualmente
# Eliminar material y volverlo a subir
```

### Errores de Base de Datos

**Error: `relation "material_chunks" does not exist`**

```bash
# Ejecutar scripts SQL
# 1. Conectar a Supabase Dashboard
# 2. SQL Editor
# 3. Pegar backend/sql/create_tables.sql
# 4. Run
```

**Error: `type "vector" does not exist`**

```bash
# Habilitar extensión pgvector
# Supabase Dashboard → Database → Extensions
# Buscar "vector" → Enable
```

### Performance Lento

**Síntoma: Queries RAG tardan >10 segundos**

```bash
# 1. Verificar índice HNSW
# Supabase SQL Editor:
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'material_chunks';

# Debe existir: material_chunks_embedding_idx

# 2. Si no existe, crearlo:
CREATE INDEX material_chunks_embedding_idx 
ON material_chunks 
USING hnsw (embedding vector_cosine_ops);

# 3. Verify chunk count
SELECT COUNT(*) FROM material_chunks;
# Si >100K, considerar partitioning
```

---

## 🔒 Seguridad en Producción

### Checklist

- [ ] HTTPS habilitado (Let's Encrypt)
- [ ] Variables de entorno en `.env` (no en código)
- [ ] `.env` en `.gitignore`
- [ ] CORS configurado solo para dominio específico
- [ ] Rate limiting en endpoints críticos
- [ ] Autenticación implementada (futuro)
- [ ] Backup automático de base de datos
- [ ] Logs rotados (logrotate)
- [ ] Firewall configurado (UFW)

### Configurar Firewall

```bash
# Permitir SSH, HTTP, HTTPS
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Denegar acceso directo a backend desde internet
sudo ufw deny 8000/tcp

# Habilitar firewall
sudo ufw enable
```

---

## 📦 Backup y Restore

### Backup de Base de Datos (Supabase)

```bash
# Backup automático en Supabase Pro
# Settings → Database → Point-in-time Recovery

# Backup manual con pg_dump (si tienes acceso directo)
pg_dump -h <supabase-host> -U postgres -d postgres > backup.sql
```

### Backup de Archivos (PDFs)

```bash
# Backup de Supabase Storage
# Dashboard → Storage → course-materials → Download all

# Backup automático con rclone (futuro)
rclone sync supabase:course-materials /backups/materials
```

---

## 🔄 CI/CD (Futuro)

### GitHub Actions

**.github/workflows/deploy.yml:**

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          cd edurag/backend
          pip install -r requirements.txt
          pytest tests/

  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Render
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}

  deploy-frontend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and deploy
        run: |
          cd edurag/frontend
          npm install
          npm run build
          # Deploy a hosting (Vercel, Netlify, etc.)
```

---

## 📚 Recursos Adicionales

- **Supabase Docs:** https://supabase.com/docs
- **Render Docs:** https://render.com/docs
- **Railway Docs:** https://docs.railway.app
- **Nginx Config:** https://nginx.org/en/docs/
- **Let's Encrypt:** https://letsencrypt.org/docs/

---

*Última actualización: Octubre 23, 2025*
*Versión: 1.0.0*
*Fin de la Documentación Técnica*
