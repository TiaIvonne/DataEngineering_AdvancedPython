#!/usr/bin/env python3
"""Script conciso para probar el ciclo completo: descarga, procesamiento y gráficos"""
import sys
from pathlib import Path

# Agregar el directorio padre al path para importar traficFines
sys.path.insert(0, str(Path(__file__).parent.parent))

from traficFines import MadridFines

def main():
    # 1. Inicializar con cache (7 días de validez)
    mf = MadridFines("MadridFines", obsolescence=7)
    
    # 2. Descargar y procesar datos (cargar múltiples años/meses)
    print("📥 Descargando datos...")
    mf.add(2025, 4)   # Añade marzo 2025 al dataset existente
    
    print(f"   ✅ Datos cargados: {len(mf._MadridFines__loaded)} meses")
    print(f"   ✅ Total registros: {len(mf._MadridFines__data):,}")
    
    # 3. Generar gráfico (debería mostrar todos los meses cargados)
    print("\n📊 Generando gráfico...")
    mf.fines_hour("pruebas/grafico_multas_hora.png")
    
    # 4. Análisis adicionales (opcional)
    print("\n📈 Análisis de calificaciones:")
    print(mf.fines_calification().head())
    
    print("\n💰 Recaudación total:")
    print(mf.total_payment())
    
    print("\n✅ Ciclo completo ejecutado correctamente")

if __name__ == "__main__":
    main()

# Source - https://stackoverflow.com/a
# Posted by rogeriopvl, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-23, License - CC BY-SA 3.0

import time
start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))

