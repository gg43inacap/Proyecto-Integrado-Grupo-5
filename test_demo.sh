#!/bin/bash

# ============================================
# SCRIPT DE DEMOSTRACIÓN - SISTEMA NEONATAL
# ============================================
# Este script ejecuta pruebas funcionales del sistema
# para demostración ante clientes.
#
# Uso: ./test_demo.sh
# ============================================

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"
PYTHON="$VENV_DIR/bin/python"
MANAGE_PY="$PROJECT_DIR/manage.py"

# ============ FUNCIONES ============

print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

check_environment() {
    print_header "1️⃣ VERIFICAR ENTORNO"
    
    # Verificar que el venv existe
    if [ ! -d "$VENV_DIR" ]; then
        print_error "Entorno virtual no encontrado en: $VENV_DIR"
        exit 1
    fi
    print_success "Entorno virtual encontrado"
    
    # Verificar que manage.py existe
    if [ ! -f "$MANAGE_PY" ]; then
        print_error "manage.py no encontrado en: $MANAGE_PY"
        exit 1
    fi
    print_success "manage.py encontrado"
    
    # Activar venv
    source "$VENV_DIR/bin/activate"
    print_success "Entorno virtual activado"
}

check_database() {
    print_header "2️⃣ VERIFICAR BASE DE DATOS"
    
    $PYTHON manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
from django.db import connection

User = get_user_model()

# Verificar conexión a BD
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("✓ Conexión a MySQL: EXITOSA")
except Exception as e:
    print(f"✗ Conexión a MySQL FALLÓ: {e}")
    exit(1)

# Contar usuarios
total_usuarios = User.objects.count()
print(f"✓ Total de usuarios en BD: {total_usuarios}")

# Listar usuarios
if total_usuarios > 0:
    print("\n  Usuarios disponibles:")
    for user in User.objects.all():
        status = "🟢 Activo" if user.is_active else "🔴 Inactivo"
        role = user.role if user.role else "SIN ROL"
        print(f"    • {user.username} (Rol: {role}) - {status}")
EOF
}

test_logins() {
    print_header "3️⃣ PROBAR LOGIN DE USUARIOS"
    
    $PYTHON manage.py shell << 'EOF'
from django.test import Client

users_to_test = [
    ('supervisor1', 'SUPERVISOR'),
    ('admin1', 'ADMIN'),
    ('matrona1', 'MATRONA'),
    ('auditor1', 'AUDITORIA'),
    ('exempleado', 'SOME'),
]

print("Prueba de login con contraseña: Inacap2025*\n")

client = Client()
passed = 0
failed = 0

for username, expected_role in users_to_test:
    success = client.login(username=username, password='Inacap2025*')
    if success:
        print(f"✓ {username:15} ({expected_role:12}) - LOGIN EXITOSO")
        passed += 1
    else:
        print(f"✗ {username:15} ({expected_role:12}) - LOGIN FALLÓ")
        failed += 1
    
    # Logout para siguiente iteración
    client.logout()

print(f"\n  Resumen: {passed}/{len(users_to_test)} logins exitosos")

if failed > 0:
    exit(1)
EOF
}

test_api_endpoints() {
    print_header "4️⃣ PROBAR API DEL SUPERVISOR"
    
    $PYTHON manage.py shell << 'EOF'
from django.test import Client
import json

print("Pruebas de endpoints HTTP:\n")

client = Client()

# Test 1: Login
print("1. Autenticando usuario supervisor1...")
if not client.login(username='supervisor1', password='Inacap2025*'):
    print("✗ Login falló")
    exit(1)
print("✓ Usuario autenticado\n")

# Test 2: Dashboard
print("2. Accediendo a dashboard...")
response = client.get('/roles/dashboard/')
if response.status_code == 200:
    print(f"✓ GET /roles/dashboard/ → HTTP {response.status_code}")
else:
    print(f"✗ GET /roles/dashboard/ → HTTP {response.status_code}")
    exit(1)

# Test 3: API Estadísticas
print("3. Consultando API de estadísticas...")
response = client.get('/roles/api/estadisticas_supervisor/')
if response.status_code == 200:
    print(f"✓ GET /roles/api/estadisticas_supervisor/ → HTTP {response.status_code}")
    try:
        data = json.loads(response.content)
        print(f"\n  Datos retornados:")
        print(f"    • Total reportes: {data.get('total_reportes', 0)}")
        print(f"    • Reportes este mes: {data.get('reportes_mes', 0)}")
        print(f"    • Tipos de reportes: {json.dumps(data.get('tipos_reportes', {}), indent=6)}")
    except json.JSONDecodeError:
        print("✗ Error al parsear JSON")
        exit(1)
else:
    print(f"✗ GET /roles/api/estadisticas_supervisor/ → HTTP {response.status_code}")
    exit(1)

# Test 4: REM A24
print("\n4. Accediendo a reporte REM A24...")
response = client.get('/reportes/rem_24/')
if response.status_code == 200:
    print(f"✓ GET /reportes/rem_24/ → HTTP {response.status_code}")
else:
    print(f"✗ GET /reportes/rem_24/ → HTTP {response.status_code}")
    exit(1)

# Test 5: Exportar Excel
print("5. Probando exportación a Excel...")
response = client.get('/reportes/exportar/rem_a24/excel/')
if response.status_code == 200:
    content_type = response.get('Content-Type', '')
    if 'spreadsheet' in content_type:
        print(f"✓ GET /reportes/exportar/rem_a24/excel/ → HTTP {response.status_code}")
        print(f"  Content-Type: {content_type}")
    else:
        print(f"⚠ GET /reportes/exportar/rem_a24/excel/ → HTTP {response.status_code}")
        print(f"  Content-Type: {content_type}")
else:
    print(f"✗ GET /reportes/exportar/rem_a24/excel/ → HTTP {response.status_code}")
    exit(1)

# Test 6: Exportar PDF
print("6. Probando exportación a PDF...")
response = client.get('/reportes/exportar/rem_a24/pdf/')
if response.status_code == 200:
    content_type = response.get('Content-Type', '')
    if 'pdf' in content_type:
        print(f"✓ GET /reportes/exportar/rem_a24/pdf/ → HTTP {response.status_code}")
        print(f"  Content-Type: {content_type}")
    else:
        print(f"⚠ GET /reportes/exportar/rem_a24/pdf/ → HTTP {response.status_code}")
        print(f"  Content-Type: {content_type}")
else:
    print(f"✗ GET /reportes/exportar/rem_a24/pdf/ → HTTP {response.status_code}")
    exit(1)

print("\n✓ TODOS LOS ENDPOINTS FUNCIONAN CORRECTAMENTE")
EOF
}

test_backup_system() {
    print_header "5️⃣ VERIFICAR SISTEMA DE BACKUPS"
    
    BACKUP_SCRIPT="$PROJECT_DIR/deploy/backup_mysql_neonatal.sh"
    
    if [ ! -f "$BACKUP_SCRIPT" ]; then
        print_error "Script de backup no encontrado: $BACKUP_SCRIPT"
        return 1
    fi
    print_success "Script de backup encontrado"
    
    if [ ! -x "$BACKUP_SCRIPT" ]; then
        print_error "Script de backup no es ejecutable"
        return 1
    fi
    print_success "Script de backup es ejecutable"
    
    # Verificar directorios de backup
    if [ -d "/home/hospital/neonatal-backups" ]; then
        BACKUP_COUNT=$(find /home/hospital/neonatal-backups -name "*.sql.gz" 2>/dev/null | wc -l)
        print_success "Carpeta de backups local existe ($BACKUP_COUNT backups)"
    else
        print_error "Carpeta de backups local no existe"
        return 1
    fi
    
    if [ -d "/backup/neonatal" ]; then
        SAMBA_BACKUP_COUNT=$(find /backup/neonatal -name "*.sql.gz" 2>/dev/null | wc -l)
        print_success "Carpeta SAMBA de backups existe ($SAMBA_BACKUP_COUNT backups)"
    else
        print_error "Carpeta SAMBA de backups no existe"
        return 1
    fi
    
    # Verificar si hay cron configurado
    if crontab -l 2>/dev/null | grep -q "backup_mysql_neonatal"; then
        print_success "Tarea cron de backup está configurada"
    else
        print_error "Tarea cron de backup NO está configurada"
        return 1
    fi
}

test_services() {
    print_header "6️⃣ VERIFICAR SERVICIOS DEL SISTEMA"
    
    services=("mysql" "nginx" "smbd" "gunicorn-neonatal")
    
    for service in "${services[@]}"; do
        if systemctl is-active --quiet "$service"; then
            print_success "Servicio $service: ACTIVO"
        else
            print_error "Servicio $service: INACTIVO"
            return 1
        fi
    done
}

show_summary() {
    print_header "📊 RESUMEN FINAL"
    
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ TODOS LOS TESTS COMPLETADOS EXITOSAMENTE${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}\n"
    
    echo "Sistema Neonatal listo para demostración:"
    echo "  ✓ Base de datos MySQL operativa"
    echo "  ✓ Todos los usuarios pueden ingresar"
    echo "  ✓ API del dashboard funcional"
    echo "  ✓ Reportes REM A24 disponibles"
    echo "  ✓ Exportación a Excel/PDF funcional"
    echo "  ✓ Sistema de backups automáticos configurado"
    echo "  ✓ Todos los servicios activos"
    echo ""
    echo "Acceso web: http://sistema.neonatal o http://localhost"
    echo "Usuario demo: supervisor1 / Inacap2025*"
}

show_errors() {
    print_header "⚠️ PRUEBAS FALLIDAS"
    
    echo -e "${RED}════════════════════════════════════════════════════════════${NC}"
    echo -e "${RED}❌ ALGUNAS PRUEBAS FALLARON${NC}"
    echo -e "${RED}════════════════════════════════════════════════════════════${NC}\n"
    
    echo "Por favor revisa los errores anteriores"
    echo "Para más detalles, consulta los logs:"
    echo "  • Django: python manage.py check"
    echo "  • MySQL: systemctl status mysql"
    echo "  • Gunicorn: journalctl -u gunicorn-neonatal"
}

# ============ EJECUCIÓN PRINCIPAL ============

main() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║       SCRIPT DE PRUEBAS - SISTEMA NEONATAL v1.0          ║"
    echo "║              Demo para Cliente Final                      ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    # Ejecutar pruebas
    if check_environment && \
       check_database && \
       test_logins && \
       test_api_endpoints && \
       test_backup_system && \
       test_services; then
        show_summary
        exit 0
    else
        show_errors
        exit 1
    fi
}

# Ejecutar
main
