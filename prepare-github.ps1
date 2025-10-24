# Script de preparación para GitHub (PowerShell)
# ================================================

Write-Host "🚀 Preparando proyecto EduRAG para GitHub..." -ForegroundColor Cyan

# 1. Verificar que estamos en la raíz del proyecto
if (-not (Test-Path "README.md")) {
    Write-Host "❌ Error: Debes ejecutar este script desde la raíz del proyecto" -ForegroundColor Red
    exit 1
}

# 2. Verificar que .gitignore existe
if (-not (Test-Path ".gitignore")) {
    Write-Host "❌ Error: .gitignore no existe" -ForegroundColor Red
    exit 1
}

Write-Host "✅ .gitignore encontrado" -ForegroundColor Green

# 3. Verificar que .env.example existe
if (-not (Test-Path ".env.example")) {
    Write-Host "📝 Creando .env.example..." -ForegroundColor Yellow
    @"
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu_supabase_anon_key
OPENAI_API_KEY=sk-tu_openai_key
"@ | Out-File -FilePath ".env.example" -Encoding UTF8
}

# 4. Verificar que .env NO está rastreado por Git
Write-Host "🔍 Verificando archivos .env..." -ForegroundColor Cyan

if (Test-Path ".git") {
    $trackedEnvFiles = git ls-files | Select-String "\.env$"
    if ($trackedEnvFiles) {
        Write-Host "⚠️  ADVERTENCIA: Archivos .env rastreados por Git:" -ForegroundColor Yellow
        $trackedEnvFiles | ForEach-Object { Write-Host "   $_" -ForegroundColor Yellow }
        Write-Host "   Ejecutando: git rm --cached .env" -ForegroundColor Yellow
        git rm --cached .env 2>$null
        git rm --cached backend/.env 2>$null
        git rm --cached frontend/.env 2>$null
    } else {
        Write-Host "✅ Archivos .env NO están en Git (correcto)" -ForegroundColor Green
    }
}

# 5. Limpiar archivos temporales
Write-Host "🧹 Limpiando archivos temporales..." -ForegroundColor Cyan

# Python cache
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Filter "*.pyo" | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "✅ Cache de Python limpiado" -ForegroundColor Green

# 6. Verificar node_modules
if (Test-Path "frontend/node_modules") {
    Write-Host "⚠️  node_modules encontrado en frontend/ (debería estar en .gitignore)" -ForegroundColor Yellow
}

if (Test-Path "mcp-server/node_modules") {
    Write-Host "⚠️  node_modules encontrado en mcp-server/ (debería estar en .gitignore)" -ForegroundColor Yellow
}

# 7. Verificar archivos críticos
Write-Host "✅ Verificando archivos críticos..." -ForegroundColor Cyan

$criticalFiles = @(
    "README.md",
    ".gitignore",
    ".env.example",
    "backend/requirements.txt",
    "backend/main.py",
    "frontend/package.json",
    "frontend/src/main.js"
)

$missingFiles = @()
foreach ($file in $criticalFiles) {
    if (-not (Test-Path $file)) {
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host "❌ Archivos faltantes:" -ForegroundColor Red
    $missingFiles | ForEach-Object { Write-Host "   $_" -ForegroundColor Red }
    exit 1
}

Write-Host "✅ Todos los archivos críticos presentes" -ForegroundColor Green

# 8. Mostrar resumen
Write-Host ""
Write-Host "📊 Resumen del repositorio:" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

$pyFiles = (Get-ChildItem -Recurse -Filter "*.py" | Where-Object { $_.FullName -notmatch "venv|__pycache__" }).Count
$vueFiles = (Get-ChildItem -Recurse -Filter "*.vue").Count
$jsFiles = (Get-ChildItem -Recurse -Filter "*.js" | Where-Object { $_.FullName -notmatch "node_modules" }).Count
$mdFiles = (Get-ChildItem -Recurse -Filter "*.md").Count

Write-Host "Python files: $pyFiles" -ForegroundColor White
Write-Host "Vue files: $vueFiles" -ForegroundColor White
Write-Host "JavaScript files: $jsFiles" -ForegroundColor White
Write-Host "Markdown docs: $mdFiles" -ForegroundColor White
Write-Host ""

# 9. Verificar configuración de entorno
Write-Host "🔐 Verificando configuración de entorno..." -ForegroundColor Cyan

if (Test-Path "backend/.env") {
    $envContent = Get-Content "backend/.env" -Raw
    if ($envContent -match "SUPABASE_URL=https://tu-proyecto") {
        Write-Host "⚠️  ADVERTENCIA: backend/.env parece tener valores de ejemplo" -ForegroundColor Yellow
        Write-Host "   Asegúrate de configurar tus credenciales reales antes de deployar" -ForegroundColor Yellow
    }
}

# 10. Verificar estado de Git
Write-Host ""
Write-Host "📍 Estado de Git:" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

if (Test-Path ".git") {
    $branch = git branch --show-current
    $lastCommit = git log -1 --pretty=format:'%h - %s (%ar)' 2>$null
    
    Write-Host "Rama actual: $branch" -ForegroundColor White
    if ($lastCommit) {
        Write-Host "Último commit: $lastCommit" -ForegroundColor White
    }
    Write-Host ""
    Write-Host "Archivos modificados:" -ForegroundColor White
    git status --short
} else {
    Write-Host "❌ No es un repositorio Git. Inicializando..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Repositorio Git inicializado" -ForegroundColor Green
}

# 11. Sugerencias finales
Write-Host ""
Write-Host "✅ Preparación completa!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Próximos pasos sugeridos:" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host "1. Revisar archivos a commitear:" -ForegroundColor White
Write-Host "   git status" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Agregar archivos al staging:" -ForegroundColor White
Write-Host "   git add ." -ForegroundColor Gray
Write-Host ""
Write-Host "3. Crear commit:" -ForegroundColor White
Write-Host "   git commit -m 'Initial commit: EduRAG complete system'" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Crear repositorio en GitHub:" -ForegroundColor White
Write-Host "   https://github.com/new" -ForegroundColor Gray
Write-Host ""
Write-Host "5. Conectar con repositorio remoto:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/usuario/edurag.git" -ForegroundColor Gray
Write-Host ""
Write-Host "6. Subir código:" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "⚠️  IMPORTANTE:" -ForegroundColor Yellow
Write-Host "   - Verifica que .env NO esté en Git" -ForegroundColor Yellow
Write-Host "   - Configura variables de entorno en Vercel/Render después" -ForegroundColor Yellow
Write-Host "   - Guarda tus API keys en un lugar seguro" -ForegroundColor Yellow
Write-Host ""
