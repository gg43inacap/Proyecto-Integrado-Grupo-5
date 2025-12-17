#!/usr/bin/env python
"""
Script de prueba para verificar los filtros de REM A24
"""

import os
import sys
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neonatal.settings')
sys.path.insert(0, '/home/hospital/Escritorio/Neonatal/Proyecto-Integrado-Grupo-5')
django.setup()

from reportes.utils import get_reporte_rem24_completo
from partos.models import RN, Parto
from datetime import date

print("\n" + "="*80)
print("🧪 PRUEBA DE FILTROS REM A24")
print("="*80 + "\n")

# Mostrar datos en BD
print("📊 ESTADO DE LA BD:")
print(f"   Total RN: {RN.objects.count()}")
print(f"   Total Partos: {Parto.objects.count()}")

# Mostrar rango de fechas en BD
rn_list = RN.objects.all()
if rn_list.exists():
    fecha_min = rn_list.earliest('fecha_nacimiento').fecha_nacimiento
    fecha_max = rn_list.latest('fecha_nacimiento').fecha_nacimiento
    print(f"   Rango de fechas: {fecha_min} a {fecha_max}\n")
else:
    print("   ⚠️  No hay datos de RN en la BD\n")

# Test 1: Sin filtros (debe mostrar datos del año actual)
print("✓ TEST 1: Sin filtros (año actual, todos los meses)")
try:
    resultado = get_reporte_rem24_completo(mes=None, anio=datetime.now().year)
    total_rn = resultado['seccion_d1']['rows'][-1][1]  # Total nacidos vivos
    print(f"   └─ RN encontrados: {total_rn}")
    print(f"   └─ Período: {resultado['periodo']}\n")
except Exception as e:
    print(f"   ❌ ERROR: {e}\n")

# Test 2: Mes específico
print("✓ TEST 2: Mes específico (Diciembre 2025)")
try:
    resultado = get_reporte_rem24_completo(mes=12, anio=2025)
    total_rn = resultado['seccion_d1']['rows'][-1][1]
    print(f"   └─ RN encontrados: {total_rn}")
    print(f"   └─ Período: {resultado['periodo']}\n")
except Exception as e:
    print(f"   ❌ ERROR: {e}\n")

# Test 3: Todos los meses de un año (mes=None, anio=2025)
print("✓ TEST 3: Todos los meses de 2025 (mes=None, anio=2025)")
try:
    resultado = get_reporte_rem24_completo(mes=None, anio=2025)
    total_rn = resultado['seccion_d1']['rows'][-1][1]
    print(f"   └─ RN encontrados: {total_rn}")
    print(f"   └─ Período: {resultado['periodo']}\n")
except Exception as e:
    print(f"   ❌ ERROR: {e}\n")

# Test 4: Año anterior (2024)
print("✓ TEST 4: Todos los meses de 2024")
try:
    resultado = get_reporte_rem24_completo(mes=None, anio=2024)
    total_rn = resultado['seccion_d1']['rows'][-1][1]
    print(f"   └─ RN encontrados: {total_rn}")
    print(f"   └─ Período: {resultado['periodo']}\n")
except Exception as e:
    print(f"   ❌ ERROR: {e}\n")

print("="*80)
print("✅ PRUEBAS COMPLETADAS")
print("="*80 + "\n")
