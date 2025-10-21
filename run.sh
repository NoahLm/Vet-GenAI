#!/bin/bash

# Script para ejecutar el dashboard fácilmente
# Uso: ./run.sh

echo "🚀 Iniciando Dashboard de Gusano Barrenador..."
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "❌ No se encontró el entorno virtual."
    echo "Por favor, crea uno primero:"
    echo "  python3 -m venv venv"
    exit 1
fi

# Activar entorno virtual
echo "✅ Activando entorno virtual..."
source venv/bin/activate

# Verificar si existen las credenciales
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo ""
    echo "⚠️  ADVERTENCIA: No se encontró el archivo de credenciales."
    echo ""
    echo "Por favor, configura tus credenciales primero:"
    echo "  1. Copia el archivo de ejemplo:"
    echo "     cp .streamlit/secrets.toml.example .streamlit/secrets.toml"
    echo ""
    echo "  2. Edita .streamlit/secrets.toml con tus credenciales de Google Cloud"
    echo ""
    echo "  3. Vuelve a ejecutar este script"
    echo ""
    echo "Ver GUIA_RAPIDA.md para más detalles."
    exit 1
fi

# Ejecutar Streamlit
echo "✅ Iniciando Streamlit..."
echo ""
streamlit run main.py
