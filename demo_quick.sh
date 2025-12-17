#!/bin/bash

# ============================================
# DEMO RÁPIDA - SISTEMA NEONATAL
# ============================================
# Script simplificado para demostración rápida
# Ejecuta solo las pruebas esenciales
#
# Uso: ./demo_quick.sh
# ============================================

cd "$(dirname "$0")" || exit 1

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════╗"
echo "║  DEMOSTRACIÓN - SISTEMA NEONATAL (QUICK)            ║"
echo "║  Pruebas rápidas para presentación al cliente       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo -e "${NC}\n"

# Activar venv
source .venv/bin/activate

echo -e "${YELLOW}Ejecutando pruebas...${NC}\n"

# Ejecutar pruebas Python
.venv/bin/python manage.py shell << 'PYTHON_EOF'
import sys
from django.test import Client
import json
from django.contrib.auth import get_user_model

User = get_user_model()

print("┌─────────────────────────────────────────────────────┐")
print("│ 1. VERIFICAR BASE DE DATOS                          │")
print("└─────────────────────────────────────────────────────┘")
print(f"✓ Usuarios en sistema: {User.objects.count()}\n")

print("┌─────────────────────────────────────────────────────┐")
print("│ 2. PRUEBAS DE LOGIN                                 │")
print("└─────────────────────────────────────────────────────┘")
client = Client()
login_results = []
for username in ['supervisor1', 'admin1', 'matrona1']:
    result = client.login(username=username, password='Inacap2025*')
    status = "✓ EXITOSO" if result else "✗ FALLÓ"
    print(f"{username}: {status}")
    login_results.append(result)
    client.logout()

print()

print("┌─────────────────────────────────────────────────────┐")
print("│ 3. PRUEBAS DE API                                   │")
print("└─────────────────────────────────────────────────────┘")
client.login(username='supervisor1', password='Inacap2025*')

# Dashboard
resp = client.get('/roles/dashboard/')
print(f"Dashboard: {resp.status_code} {'✓' if resp.status_code == 200 else '✗'}")

# API Estadísticas
resp = client.get('/roles/api/estadisticas_supervisor/')
print(f"API Estadísticas: {resp.status_code} {'✓' if resp.status_code == 200 else '✗'}")
if resp.status_code == 200:
    data = json.loads(resp.content)
    print(f"  └─ Total reportes: {data.get('total_reportes', 0)}")

# REM A24
resp = client.get('/reportes/rem_24/')
print(f"Reporte REM A24: {resp.status_code} {'✓' if resp.status_code == 200 else '✗'}")

# Excel export
resp = client.get('/reportes/exportar/rem_a24/excel/')
print(f"Exportar Excel: {resp.status_code} {'✓' if resp.status_code == 200 else '✗'}")

# PDF export
resp = client.get('/reportes/exportar/rem_a24/pdf/')
print(f"Exportar PDF: {resp.status_code} {'✓' if resp.status_code == 200 else '✗'}")

print()

print("┌─────────────────────────────────────────────────────┐")
print("│ 4. RESUMEN                                          │")
print("└─────────────────────────────────────────────────────┘")

if all(login_results):
    print("✓ TODOS LOS TESTS COMPLETADOS")
    print("\nAcceso web disponible en:")
    print("  URL: http://sistema.neonatal (o http://localhost)")
    print("  Usuario: supervisor1")
    print("  Contraseña: Inacap2025*")
    sys.exit(0)
else:
    print("✗ ALGUNOS TESTS FALLARON")
    sys.exit(1)
PYTHON_EOF

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}═══════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ SISTEMA LISTO PARA DEMOSTRACIÓN${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
else
    echo -e "\n${RED}═══════════════════════════════════════════════════════${NC}"
    echo -e "${RED}❌ ERRORES EN LAS PRUEBAS${NC}"
    echo -e "${RED}═══════════════════════════════════════════════════════${NC}"
    exit 1
fi
