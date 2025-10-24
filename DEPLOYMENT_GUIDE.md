# Guía de Despliegue - Proyecto EduRAG

## Tabla de Contenidos
1. [Opción 1: Vercel + Render + Supabase (RECOMENDADO)](#opción-1-vercel--render--supabase-recomendado)
2. [Opción 2: Netlify + Railway + Supabase](#opción-2-netlify--railway--supabase)
3. [Opción 3: Todo en Render (Full-Stack)](#opción-3-todo-en-render-full-stack)
4. [Opción 4: AWS (Avanzado)](#opción-4-aws-avanzado)
5. [Opción 5: DigitalOcean Droplet (VPS)](#opción-5-digitalocean-droplet-vps)
6. [Comparación de Opciones](#comparación-de-opciones)

---

## Opción 1: Vercel + Render + Supabase (RECOMENDADO) ✅

**Stack de Despliegue:**
- **Frontend:** Vercel (CDN Global)
- **Backend:** Render (Container)
- **Database:** Supabase (PostgreSQL + Storage)
- **Costo:** $0-7/mes

### Ventajas:
✅ Gratis para empezar
✅ Deploy automático desde Git
✅ SSL/HTTPS automático
✅ Fácil de configurar
✅ Excelente performance (CDN global)

### Paso a Paso:

#### A. Frontend en Vercel

1. **Crear cuenta en Vercel:**
   - Ir a https://vercel.com
   - Sign up con GitHub

2. **Preparar frontend para producción:**
```bash
cd frontend

# Crear archivo .env.production
VITE_API_URL=https://tu-backend.onrender.com

# Verificar que build funciona
npm run build
```

3. **Configurar Vercel:**
   - En Vercel dashboard: "Add New Project"
   - Importar repositorio de GitHub
   - Configurar:
     - **Framework Preset:** Vite
     - **Root Directory:** `frontend/`
     - **Build Command:** `npm run build`
     - **Output Directory:** `dist`
     - **Install Command:** `npm install`
   - Agregar variables de entorno:
     - `VITE_API_URL`: URL del backend (configurar después)

4. **Deploy:**
   - Click "Deploy"
   - Esperar 2-3 minutos
   - Obtendrás URL: `https://edurag.vercel.app`

#### B. Backend en Render

1. **Crear cuenta en Render:**
   - Ir a https://render.com
   - Sign up con GitHub

2. **Preparar backend:**
```bash
cd backend

# Crear archivo requirements.txt (si no existe)
fastapi==0.104.1
uvicorn[standard]==0.24.0
supabase==2.0.3
pydantic==2.5.0
pydantic[email]
python-multipart==0.0.6
openai==1.3.0
langchain==0.0.335
pdfplumber==0.10.3
python-dotenv==1.0.0

# Crear archivo render.yaml (opcional, para configuración)
```

3. **Crear `render.yaml` en raíz del proyecto:**
```yaml
services:
  - type: web
    name: edurag-backend
    runtime: python
    buildCommand: "cd backend && pip install -r requirements.txt"
    startCommand: "cd backend && gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_KEY
        sync: false
      - key: OPENAI_API_KEY
        sync: false
```

4. **Agregar gunicorn a requirements.txt:**
```txt
gunicorn==21.2.0
```

5. **Configurar Render:**
   - En Render dashboard: "New +" → "Web Service"
   - Conectar repositorio GitHub
   - Configurar:
     - **Name:** edurag-backend
     - **Root Directory:** `backend/`
     - **Runtime:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000`
     - **Plan:** Free (o Starter $7/mes para always-on)

6. **Agregar variables de entorno en Render:**
   - SUPABASE_URL: `https://xxxxx.supabase.co`
   - SUPABASE_KEY: `tu_supabase_anon_key`
   - OPENAI_API_KEY: `sk-xxxxx`

7. **Deploy:**
   - Click "Create Web Service"
   - Esperar 5-10 minutos
   - Obtendrás URL: `https://edurag-backend.onrender.com`

#### C. Supabase (Ya configurado)

1. **Verificar Supabase está funcionando:**
   - Ir a https://supabase.com/dashboard
   - Verificar que base de datos tiene todas las tablas
   - Verificar que Storage bucket `course-materials` existe

2. **Obtener credenciales:**
   - Settings → API
   - Copiar `URL` y `anon public` key

#### D. Actualizar URLs y Re-Deploy

1. **Actualizar frontend con URL del backend:**
   - En Vercel → Settings → Environment Variables
   - Actualizar `VITE_API_URL` con `https://edurag-backend.onrender.com`
   - Re-deploy (automático)

2. **Actualizar CORS en backend:**
```python
# backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://edurag.vercel.app",  # Agregar tu URL de Vercel
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

3. **Commit y push cambios:**
```bash
git add .
git commit -m "Configure production CORS"
git push
```

#### E. Verificar Deployment

1. **Probar frontend:**
   - Ir a `https://edurag.vercel.app`
   - Intentar login

2. **Probar backend:**
   - Ir a `https://edurag-backend.onrender.com/docs`
   - Verificar Swagger UI funciona

3. **Probar integración completa:**
   - Crear un estudiante
   - Subir un material PDF
   - Probar chat RAG

---

## Opción 2: Netlify + Railway + Supabase

**Stack de Despliegue:**
- **Frontend:** Netlify (similar a Vercel)
- **Backend:** Railway (similar a Render, pero $5/mes mínimo)
- **Database:** Supabase
- **Costo:** $5-12/mes

### Ventajas:
✅ Netlify tiene Forms integrados (útil para contacto)
✅ Railway despliegue muy rápido
✅ Railway incluye PostgreSQL (alternativa a Supabase)

### Paso a Paso:

#### A. Frontend en Netlify

1. **Crear cuenta:**
   - https://netlify.com → Sign up con GitHub

2. **Deploy:**
   - "Add new site" → "Import from Git"
   - Seleccionar repo
   - Configurar:
     - **Base directory:** `frontend/`
     - **Build command:** `npm run build`
     - **Publish directory:** `frontend/dist`
   - Environment variables: `VITE_API_URL`

3. **Custom domain (opcional):**
   - Site settings → Domain management
   - Agregar dominio custom

#### B. Backend en Railway

1. **Crear cuenta:**
   - https://railway.app → Sign up con GitHub

2. **Deploy:**
   - "New Project" → "Deploy from GitHub repo"
   - Seleccionar repo
   - Railway detecta Python automáticamente
   - Agregar variables de entorno

3. **Costo:**
   - $5/mes por 500 horas (servidor always-on)

---

## Opción 3: Todo en Render (Full-Stack)

**Stack de Despliegue:**
- **Frontend + Backend:** Render (ambos en Render)
- **Database:** Supabase
- **Costo:** $0-14/mes

### Ventajas:
✅ Todo en un solo proveedor (simplicidad)
✅ Un solo dashboard
✅ Configuración unificada

### Paso a Paso:

1. **Backend en Render** (igual que Opción 1B)

2. **Frontend en Render (como Static Site):**
   - "New +" → "Static Site"
   - Conectar repo
   - Configurar:
     - **Build command:** `cd frontend && npm install && npm run build`
     - **Publish directory:** `frontend/dist`
   - Environment variables: `VITE_API_URL`

3. **Ventaja:** Deploy coordinado
4. **Desventaja:** Frontend no está en CDN global (más lento que Vercel/Netlify)

---

## Opción 4: AWS (Avanzado)

**Stack de Despliegue:**
- **Frontend:** S3 + CloudFront (CDN)
- **Backend:** EC2 o Elastic Beanstalk o Lambda
- **Database:** RDS PostgreSQL
- **Costo:** $20-100/mes

### Ventajas:
✅ Escalabilidad ilimitada
✅ Control total
✅ Servicios integrados (SES, SNS, etc.)

### Desventajas:
❌ Configuración compleja
❌ Curva de aprendizaje empinada
❌ Más costoso

### Paso a Paso Simplificado:

#### A. Frontend en S3 + CloudFront

```bash
# Build frontend
cd frontend
npm run build

# Instalar AWS CLI
pip install awscli

# Configurar AWS
aws configure

# Crear bucket S3
aws s3 mb s3://edurag-frontend

# Subir archivos
aws s3 sync dist/ s3://edurag-frontend --acl public-read

# Configurar bucket como website
aws s3 website s3://edurag-frontend --index-document index.html
```

#### B. Backend en EC2

1. Lanzar instancia EC2 (Ubuntu 22.04)
2. SSH a instancia
3. Instalar Python, Git, Nginx
4. Clonar repo
5. Configurar Nginx como reverse proxy
6. Usar systemd para auto-start

**Comando de setup:**
```bash
# SSH a EC2
ssh -i key.pem ubuntu@ec2-xx-xx-xx-xx.compute.amazonaws.com

# Instalar dependencias
sudo apt update
sudo apt install python3-pip nginx git

# Clonar repo
git clone https://github.com/usuario/edurag.git
cd edurag/backend

# Instalar requirements
pip3 install -r requirements.txt

# Configurar Nginx
sudo nano /etc/nginx/sites-available/edurag

# Contenido:
# server {
#     listen 80;
#     server_name api.edurag.com;
#     location / {
#         proxy_pass http://127.0.0.1:8000;
#     }
# }

# Iniciar backend con systemd
sudo nano /etc/systemd/system/edurag.service

# Contenido:
# [Unit]
# Description=EduRAG Backend
# After=network.target
# 
# [Service]
# User=ubuntu
# WorkingDirectory=/home/ubuntu/edurag/backend
# ExecStart=/usr/local/bin/gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
# Restart=always
# 
# [Install]
# WantedBy=multi-user.target

sudo systemctl enable edurag
sudo systemctl start edurag
```

---

## Opción 5: DigitalOcean Droplet (VPS)

**Stack de Despliegue:**
- **Frontend + Backend:** Droplet (VPS)
- **Database:** Managed PostgreSQL de DigitalOcean o Supabase
- **Costo:** $6-12/mes

### Ventajas:
✅ Control total del servidor
✅ Precio fijo predecible
✅ Más barato que AWS para proyectos pequeños

### Paso a Paso:

1. **Crear Droplet:**
   - https://digitalocean.com
   - Create → Droplets
   - Choose: Ubuntu 22.04, Basic plan ($6/mes)
   - Add SSH key

2. **Setup inicial:**
```bash
# SSH al droplet
ssh root@your-droplet-ip

# Actualizar sistema
apt update && apt upgrade -y

# Instalar dependencias
apt install python3-pip nginx git nodejs npm postgresql-client -y

# Crear usuario no-root
adduser edurag
usermod -aG sudo edurag
su - edurag
```

3. **Deploy backend:**
```bash
# Clonar repo
git clone https://github.com/usuario/edurag.git
cd edurag/backend

# Crear venv
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
pip install gunicorn

# Configurar .env
nano .env
# Agregar variables de entorno

# Probar backend
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

4. **Deploy frontend:**
```bash
cd ../frontend
npm install
npm run build

# Mover build a Nginx
sudo cp -r dist/* /var/www/html/
```

5. **Configurar Nginx:**
```bash
sudo nano /etc/nginx/sites-available/edurag

# Contenido:
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /var/www/html;
        try_files $uri /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Activar sitio
sudo ln -s /etc/nginx/sites-available/edurag /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

6. **SSL con Let's Encrypt:**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## Comparación de Opciones

| Opción | Frontend | Backend | Database | Costo/Mes | Dificultad | Tiempo Setup | Recomendado Para |
|--------|----------|---------|----------|-----------|------------|--------------|------------------|
| **1. Vercel + Render + Supabase** | Vercel | Render | Supabase | $0-7 | ⭐ Fácil | 30 min | **MVP, Estudiantes** ✅ |
| **2. Netlify + Railway + Supabase** | Netlify | Railway | Supabase | $5-12 | ⭐ Fácil | 30 min | Alternativa a #1 |
| **3. Todo en Render** | Render | Render | Supabase | $0-14 | ⭐ Fácil | 20 min | Simplicidad |
| **4. AWS** | S3+CloudFront | EC2/Lambda | RDS | $20-100 | ⭐⭐⭐⭐ Difícil | 3-5 horas | Empresas grandes |
| **5. DigitalOcean** | Droplet | Droplet | Managed DB | $6-12 | ⭐⭐⭐ Medio | 1-2 horas | Control total |

---

## Recomendación Final

### Para este proyecto (EduRAG), recomiendo **Opción 1**:

**Vercel (Frontend) + Render (Backend) + Supabase (Database)**

**Razones:**
1. ✅ **Gratis para empezar** ($0/mes en fase de desarrollo)
2. ✅ **Deploy automático desde Git** (push → deploy automático)
3. ✅ **SSL/HTTPS gratis** (certificados automáticos)
4. ✅ **Fácil de configurar** (30 minutos total)
5. ✅ **Performance excelente** (Vercel CDN global)
6. ✅ **Escalable** (soporta 100-1000 usuarios sin cambios)
7. ✅ **Logs y monitoring incluidos**
8. ✅ **Ideal para portafolio/proyecto académico**

---

## Checklist Pre-Deployment

Antes de deployar, asegúrate de:

### Frontend:
- [ ] `npm run build` funciona sin errores
- [ ] Variables de entorno configuradas en `.env.production`
- [ ] CORS configurado correctamente en backend
- [ ] URLs de API apuntan a producción (no localhost)

### Backend:
- [ ] `requirements.txt` actualizado
- [ ] Todas las variables de entorno identificadas
- [ ] CORS permite origen de frontend de producción
- [ ] Health check endpoint (`/` o `/health`) retorna 200
- [ ] gunicorn instalado

### Database:
- [ ] Todas las tablas creadas en Supabase
- [ ] pgvector extension activada
- [ ] Funciones SQL (match_material_chunks) creadas
- [ ] Storage bucket creado
- [ ] API keys copiadas

### Git:
- [ ] `.gitignore` actualizado (archivo que acabo de crear)
- [ ] `.env` NO está en Git
- [ ] Commit todos los cambios
- [ ] Push a GitHub

---

## Script de Deployment Rápido

```bash
#!/bin/bash
# deploy.sh - Script para deployment rápido

echo "🚀 EduRAG Deployment Script"

# 1. Verificar que estamos en rama main
echo "📍 Verificando rama..."
git checkout main

# 2. Pull últimos cambios
echo "📥 Pulling cambios..."
git pull origin main

# 3. Build frontend local (verificación)
echo "🔨 Building frontend..."
cd frontend
npm install
npm run build
cd ..

# 4. Verificar backend
echo "🐍 Verificando backend..."
cd backend
pip install -r requirements.txt
python -c "import fastapi; print('✅ FastAPI OK')"
cd ..

# 5. Commit y push
echo "📤 Committing y pushing..."
git add .
git commit -m "Deploy: $(date +'%Y-%m-%d %H:%M:%S')"
git push origin main

echo "✅ Deploy iniciado en Vercel y Render!"
echo "📊 Vercel: https://vercel.com/dashboard"
echo "📊 Render: https://dashboard.render.com"
```

Guarda este script como `deploy.sh` y ejecútalo con `bash deploy.sh`.

---

## URLs Útiles

- **Vercel Dashboard:** https://vercel.com/dashboard
- **Render Dashboard:** https://dashboard.render.com
- **Supabase Dashboard:** https://supabase.com/dashboard
- **Netlify Dashboard:** https://app.netlify.com
- **Railway Dashboard:** https://railway.app/dashboard

---

¿Necesitas ayuda con alguna opción específica? ¡Avísame!
