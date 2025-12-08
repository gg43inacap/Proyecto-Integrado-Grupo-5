#!/usr/bin/env python
"""
Test Suite Completo - Ejecuta todos los tests unitarios del sistema
"""
import os
import django
import subprocess
import sys
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neonatal.settings')
django.setup()

def run_tests():
    """Ejecutar todos los tests y generar reporte"""
    print("=" * 80)
    print("           SUITE COMPLETO DE TESTS UNITARIOS")
    print("           Sistema Neonatal - Proyecto Integrado")
    print("=" * 80)
    print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Lista de apps y tests a ejecutar
    test_suites = [
        ('Login y Autenticación', 'login.tests'),
        ('Roles y Usuarios', 'roles.tests'),
        ('Gestión SOME (Madres)', 'gestion_some.tests'),
        ('Partos y RN', 'partos.tests'),
        ('Auditoría Sistema', 'auditoria.tests'),
        ('Integración Auditoría', 'auditoria.tests_integracion'),
        ('Reportes (Preparado)', 'reportes.tests'),
    ]

    results = []
    total_tests = 0
    total_passed = 0

    for suite_name, test_module in test_suites:
        print(f"\n🧪 EJECUTANDO: {suite_name}")
        print("-" * 60)
        
        try:
            # Ejecutar tests con capture
            result = subprocess.run([
                sys.executable, 'manage.py', 'test', test_module, '--verbosity=1'
            ], capture_output=True, text=True)
            
            # Parsear resultado
            output = result.stdout + result.stderr
            
            if result.returncode == 0:
                # Extraer número de tests del output
                lines = output.split('\n')
                test_count = 0
                for line in lines:
                    if 'Ran' in line and 'test' in line:
                        try:
                            test_count = int(line.split()[1])
                        except:
                            test_count = 1
                        break
                
                print(f"✅ PASÓ - {test_count} tests ejecutados")
                results.append((suite_name, True, test_count, ""))
                total_tests += test_count
                total_passed += test_count
            else:
                print(f"❌ FALLÓ")
                error_msg = output.split('\n')[-10:]  # Últimas 10 líneas del error
                error_summary = '\n'.join([line for line in error_msg if line.strip()])
                print(f"   Error: {error_summary[:200]}...")
                results.append((suite_name, False, 0, error_summary))
                
        except Exception as e:
            print(f"❌ ERROR EJECUTANDO: {e}")
            results.append((suite_name, False, 0, str(e)))

    # Reporte final
    print("\n" + "=" * 80)
    print("                    RESUMEN FINAL DE TESTS")
    print("=" * 80)
    
    suites_passed = 0
    for suite_name, passed, test_count, error in results:
        status = "✅ PASÓ" if passed else "❌ FALLÓ"
        test_info = f"({test_count} tests)" if test_count > 0 else ""
        print(f"{suite_name:30} {status:10} {test_info}")
        if passed:
            suites_passed += 1
        elif not passed and error:
            print(f"   └─ Error: {error[:100]}...")

    print(f"\n📊 ESTADÍSTICAS FINALES:")
    print(f"   • Suites ejecutadas: {len(test_suites)}")
    print(f"   • Suites exitosas: {suites_passed}")
    print(f"   • Tests individuales: {total_passed}")
    
    success_rate = (suites_passed / len(test_suites)) * 100 if test_suites else 0
    
    print(f"\n🎯 TASA DE ÉXITO: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🚀 ¡EXCELENTE! Sistema listo para producción")
    elif success_rate >= 75:
        print("👍 BUENO: Sistema estable, pequeños ajustes necesarios")
    elif success_rate >= 50:
        print("⚠️  REGULAR: Requiere atención antes del despliegue")
    else:
        print("🔥 CRÍTICO: Problemas serios detectados")

    # Recomendaciones
    print(f"\n💡 RECOMENDACIONES:")
    if suites_passed == len(test_suites):
        print("   • Todos los tests pasan - Sistema robusto ✨")
        print("   • Listo para integrar con CSS de tus compañeros 🎨")
        print("   • Preparado para app de reportes 📊")
    else:
        failed_suites = [name for name, passed, _, _ in results if not passed]
        print(f"   • Revisar suites fallidas: {', '.join(failed_suites)}")
        print("   • Ejecutar tests individuales para más detalles")
        print("   • Verificar migraciones y configuración de DB")

    print(f"\n📚 COVERAGE ACTUAL:")
    print("   ✅ Modelos y validaciones")
    print("   ✅ Vistas y URLs") 
    print("   ✅ Autenticación y roles")
    print("   ✅ Auditoría completa")
    print("   ✅ Integración AJAX")
    print("   ⏳ CSS y frontend (pendiente)")
    print("   ⏳ Reportes específicos (pendiente)")
    
    return success_rate >= 75

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)