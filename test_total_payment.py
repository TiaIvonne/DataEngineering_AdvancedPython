#!/usr/bin/env python3
import sys
sys.path.insert(0, 'traficFines')
from madridFines import MadridFines
import pandas as pd

print("=" * 60)
print("PRUEBA: total_payment()")
print("=" * 60)

# Crear objeto y cargar datos
multas = MadridFines("TestApp", 30)
print("\n📅 Cargando datos:")
print("   - Abril 2023")
multas.add(2023, 4)
print("   - Abril 2024")
multas.add(2024, 4)
print("   - Abril 2025")
multas.add(2025, 4)

print(f"\n✅ Total de filas cargadas: {len(multas._MadridFines__data):,}")
print(f"✅ Meses cargados: {multas._MadridFines__loaded}")

# Probar total_payment
print("\n📊 Ejecutando total_payment()...")
try:
    resultado = multas.total_payment()
    
    print("\n✅ Método ejecutado correctamente")
    print(f"\n📋 Tipo del resultado: {type(resultado)}")
    print(f"📋 Shape del DataFrame: {resultado.shape}")
    
    print("\n" + "=" * 60)
    print("DATAFRAME COMPLETO:")
    print("=" * 60)
    print(resultado)
    
    print("\n" + "=" * 60)
    print("INFORMACIÓN DEL DATAFRAME:")
    print("=" * 60)
    print(f"Columnas: {list(resultado.columns)}")
    print(f"Total de filas: {len(resultado)}")
    
    # Verificar estructura esperada
    print("\n" + "=" * 60)
    print("VERIFICACIÓN:")
    print("=" * 60)
    
    # Verificar que tiene las columnas esperadas
    columnas_esperadas = {'MES', 'ANIO', 'rec_maxima', 'rec_minima'}
    columnas_encontradas = set(resultado.columns)
    
    if 'MES' in resultado.columns:
        print("✅ Columna 'MES' presente")
    else:
        print("⚠️  Columna 'MES' NO presente")
    
    if 'ANIO' in resultado.columns:
        print("✅ Columna 'ANIO' presente")
    else:
        print("⚠️  Columna 'ANIO' NO presente")
    
    if 'rec_maxima' in resultado.columns:
        print("✅ Columna 'rec_maxima' presente")
    else:
        print("⚠️  Columna 'rec_maxima' NO presente")
    
    if 'rec_minima' in resultado.columns:
        print("✅ Columna 'rec_minima' presente")
    else:
        print("⚠️  Columna 'rec_minima' NO presente")
    
    # Verificar que rec_minima es aproximadamente la mitad de rec_maxima
    if 'rec_maxima' in resultado.columns and 'rec_minima' in resultado.columns:
        # Filtrar solo las filas donde tenemos MES y ANIO (si están en el resultado)
        if 'MES' in resultado.columns and 'ANIO' in resultado.columns:
            print("\n📊 Verificación de cálculos (primeras filas con MES y ANIO):")
            muestra = resultado[['MES', 'ANIO', 'rec_maxima', 'rec_minima']].head()
            print(muestra)
            
            # Verificar relación rec_minima = rec_maxima * 0.5
            if len(muestra) > 0:
                for idx, row in muestra.iterrows():
                    if pd.notna(row['rec_maxima']) and pd.notna(row['rec_minima']):
                        esperado = row['rec_maxima'] * 0.5
                        diferencia = abs(row['rec_minima'] - esperado)
                        if diferencia < 0.01:  # Tolerancia para errores de punto flotante
                            print(f"✅ Fila {idx}: rec_minima = rec_maxima * 0.5 ✓")
                        else:
                            print(f"⚠️  Fila {idx}: rec_minima ({row['rec_minima']}) != rec_maxima * 0.5 ({esperado})")
    
    # Verificar valores NaN
    if resultado.isna().sum().sum() == 0:
        print("\n✅ No hay valores NaN")
    else:
        print(f"\n⚠️  Hay {resultado.isna().sum().sum()} valores NaN")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)

