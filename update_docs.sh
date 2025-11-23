#!/bin/bash
# Script para actualizar la documentación HTML después de cambios en docstrings

echo "📚 Regenerando documentación..."
pdoc -o docs_html traficFines

if [ $? -eq 0 ]; then
    echo "✅ Documentación actualizada en docs_html/"
    echo "🌐 Abriendo en Firefox..."
    open -a Firefox docs_html/traficFines.html
else
    echo "❌ Error al generar documentación"
    exit 1
fi

