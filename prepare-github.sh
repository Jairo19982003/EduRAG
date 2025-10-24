#!/bin/bash
# Script de preparación para subir a GitHub

echo "🚀 Preparando proyecto EduRAG para GitHub..."

# 1. Verificar que estamos en la raíz del proyecto
if [ ! -f "README.md" ]; then
    echo "❌ Error: Debes ejecutar este script desde la raíz del proyecto"
    exit 1
fi

# 2. Crear .env.example si no existe
if [ ! -f ".env.example" ]; then
    echo "📝 Creando .env.example..."
    cat > .env.example << 'EOF'
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu_supabase_anon_key
OPENAI_API_KEY=sk-tu_openai_key
EOF
fi

# 3. Verificar que .env NO está en Git
if git ls-files --error-unmatch .env 2>/dev/null; then
    echo "⚠️  ADVERTENCIA: .env está rastreado por Git!"
    echo "Ejecutando: git rm --cached .env"
    git rm --cached .env
    git rm --cached backend/.env 2>/dev/null
    git rm --cached frontend/.env 2>/dev/null
fi

# 4. Limpiar archivos innecesarios
echo "🧹 Limpiando archivos temporales..."

# Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name "*.pyo" -delete 2>/dev/null

# Node modules (no deberían estar, pero por si acaso)
echo "📦 Verificando node_modules..."
if [ -d "frontend/node_modules" ]; then
    echo "⚠️  node_modules encontrado en frontend/ (debe estar en .gitignore)"
fi

if [ -d "mcp-server/node_modules" ]; then
    echo "⚠️  node_modules encontrado en mcp-server/ (debe estar en .gitignore)"
fi

# 5. Verificar archivos críticos
echo "✅ Verificando archivos críticos..."

critical_files=(
    "README.md"
    ".gitignore"
    ".env.example"
    "backend/requirements.txt"
    "backend/main.py"
    "frontend/package.json"
    "frontend/src/main.js"
)

missing_files=()
for file in "${critical_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo "❌ Archivos faltantes:"
    printf '%s\n' "${missing_files[@]}"
    exit 1
fi

echo "✅ Todos los archivos críticos presentes"

# 6. Verificar que .gitignore existe
if [ ! -f ".gitignore" ]; then
    echo "❌ Error: .gitignore no existe"
    exit 1
fi

echo "✅ .gitignore encontrado"

# 7. Mostrar resumen de archivos a subir
echo ""
echo "📊 Resumen del repositorio:"
echo "================================"

# Contar archivos por tipo
echo "Python files: $(find . -name "*.py" -not -path "*/venv/*" -not -path "*/__pycache__/*" | wc -l)"
echo "Vue files: $(find . -name "*.vue" | wc -l)"
echo "JavaScript files: $(find . -name "*.js" -not -path "*/node_modules/*" | wc -l)"
echo "Markdown docs: $(find . -name "*.md" | wc -l)"
echo ""

# 8. Verificar que las variables de entorno están configuradas
echo "🔐 Verificando configuración de entorno..."

if [ -f "backend/.env" ]; then
    if grep -q "SUPABASE_URL=https://tu-proyecto" "backend/.env"; then
        echo "⚠️  ADVERTENCIA: backend/.env parece tener valores de ejemplo"
        echo "   Asegúrate de configurar tus credenciales reales antes de deployar"
    fi
fi

# 9. Verificar estado de Git
echo ""
echo "📍 Estado de Git:"
echo "================================"

if [ -d ".git" ]; then
    echo "Rama actual: $(git branch --show-current)"
    echo "Último commit: $(git log -1 --pretty=format:'%h - %s (%ar)')"
    echo ""
    echo "Archivos modificados:"
    git status --short
else
    echo "❌ No es un repositorio Git. Inicializando..."
    git init
    echo "✅ Repositorio Git inicializado"
fi

# 10. Sugerencias finales
echo ""
echo "✅ Preparación completa!"
echo ""
echo "📝 Próximos pasos sugeridos:"
echo "================================"
echo "1. Revisar archivos a commitear:"
echo "   git status"
echo ""
echo "2. Agregar archivos al staging:"
echo "   git add ."
echo ""
echo "3. Crear commit:"
echo "   git commit -m 'Initial commit: EduRAG complete system'"
echo ""
echo "4. Crear repositorio en GitHub:"
echo "   https://github.com/new"
echo ""
echo "5. Conectar con repositorio remoto:"
echo "   git remote add origin https://github.com/usuario/edurag.git"
echo ""
echo "6. Subir código:"
echo "   git push -u origin main"
echo ""
echo "⚠️  IMPORTANTE:"
echo "   - Verifica que .env NO esté en Git"
echo "   - Configura variables de entorno en Vercel/Render después"
echo "   - Guarda tus API keys en un lugar seguro"
echo ""
