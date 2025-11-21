#!/usr/bin/env python3
import sys
sys.path.insert(0, 'traficFines')
from madridFines import MadridFines

# Crear objeto
multas = MadridFines("TestApp", 30)

# Probar load con Mayo 2025
df = multas._MadridFines__load(2024, 4, multas._MadridFines__cacheurl)

multas._MadridFines__clean(df)

print("Test load and clean passed")
print(f"✅ Filas: {len(df)}, Columnas: {len(df.columns)}")
print(f"📋 Columnas: {list(df.columns)}")


