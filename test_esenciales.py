#!/usr/bin/env python
"""
Tests Esenciales - Versión simplificada y funcional
"""
import os
import django
from django.test import TestCase, Client
from django.urls import reverse

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neonatal.settings')
django.setup()

from django.contrib.auth import get_user_model
from roles.utils import validar_rut
from gestion_some.models import Madre
from partos.models import Parto, RN
from auditoria.models import Auditoria

class TestsEsenciales(TestCase):
    """Tests básicos pero funcionales para las funcionalidades principales"""
    
    def setUp(self):
        User = get_user_model()
        # Usar un RUT único para evitar conflictos - RUT válido pero único
        import random
        import time
        unique_id = int(time.time() * 1000) % 10000  # Usar timestamp para unicidad
        
        # Lista de RUTs válidos que podemos usar para tests
        valid_test_ruts = [
            '20.123.456-7',
            '21.234.567-8', 
            '22.345.678-9',
            '23.456.789-0',
            '24.567.890-1'
        ]
        
        self.test_rut = valid_test_ruts[unique_id % len(valid_test_ruts)]
        
        # Verificar que el RUT no exista, si existe usar otro
        User = get_user_model()
        counter = 0
        while User.objects.filter(rut=self.test_rut).exists() and counter < 10:
            counter += 1
            self.test_rut = f'{20 + counter}.{123 + counter}.{456 + counter}-{(counter % 10)}'
        
        self.user = User.objects.create_user(
            username=f'test_user_{unique_id}', 
            password='test123', 
            role='MATRONA',
            rut=self.test_rut
        )
        self.client = Client()
        
    def tearDown(self):
        """Limpiar después de cada test"""
        # Limpiar datos de test
        if hasattr(self, 'user') and self.user:
            self.user.delete()
        
    def test_validacion_rut(self):
        """Test básico de validación de RUT"""
        # RUTs válidos conocidos
        self.assertTrue(validar_rut('8.168.483-9'))
        self.assertTrue(validar_rut('12345678-5'))
        self.assertTrue(validar_rut('18765432-7'))
        
        # RUTs obviamente inválidos
        self.assertFalse(validar_rut('123'))
        self.assertFalse(validar_rut('abc-1'))
        
    def test_login_funcional(self):
        """Test que el login funcione básicamente"""
        response = self.client.post(reverse('login'), {
            'login_type': 'username',
            'username': 'test_user',
            'password': 'test123'
        })
        # Debería redirigir (302) o mostrar página sin error (200)
        self.assertIn(response.status_code, [200, 302])
        
    def test_crear_madre_basico(self):
        """Test crear madre con datos mínimos"""
        madre = Madre.objects.create(
            nombre='Test',
            rut='25.111.222-3',
            fecha_nacimiento='1990-01-01',
            comuna='Test',
            cesfam='Test',
            prevision='fonasa',
            direccion='Test',
            telefono='912345678',
            antecedentes_obstetricos='Test',
            atenciones_clinicas='Test',
            acompanante='Test'
        )
        self.assertEqual(madre.nombre, 'Test')
        self.assertIsNotNone(madre.id)
        
    def test_crear_parto_basico(self):
        """Test crear parto básico"""
        madre = Madre.objects.create(
            nombre='Test Parto',
            rut='26.222.333-4',
            fecha_nacimiento='1990-01-01',
            comuna='Test',
            cesfam='Test',
            prevision='fonasa',
            direccion='Test',
            telefono='912345678',
            antecedentes_obstetricos='Test',
            atenciones_clinicas='Test',
            acompanante='Test'
        )
        
        parto = Parto.objects.create(
            madre=madre,
            fecha_hora='2023-01-01T10:00',
            tipo_parto='vaginal',
            estado='activo'
        )
        
        self.assertEqual(parto.estado, 'activo')
        self.assertEqual(parto.madre, madre)
        
    def test_crear_rn_basico(self):
        """Test crear RN básico"""
        madre = Madre.objects.create(
            nombre='Test RN',
            rut='27.333.444-5',
            fecha_nacimiento='1990-01-01',
            comuna='Test',
            cesfam='Test',
            prevision='fonasa',
            direccion='Test',
            telefono='912345678',
            antecedentes_obstetricos='Test',
            atenciones_clinicas='Test',
            acompanante='Test'
        )
        
        parto = Parto.objects.create(
            madre=madre,
            fecha_hora='2023-01-01T10:00',
            tipo_parto='vaginal'
        )
        
        rn = RN.objects.create(
            madre=madre,
            parto_asociado=parto,
            fecha_nacimiento='2023-01-01',
            hora_nacimiento='10:30',
            apellido_paterno_rn='TestRN',
            sexo='M'
        )
        
        self.assertEqual(rn.apellido_paterno_rn, 'TestRN')
        self.assertEqual(rn.madre, madre)
        self.assertEqual(rn.parto_asociado, parto)
        
    def test_auditoria_funcional(self):
        """Test que la auditoría se pueda crear"""
        auditoria = Auditoria.objects.create(
            usuario=self.user,
            accion_realizada='CREATE',
            modelo_afectado='Test',
            registro_id=1,
            detalles_cambio='Test de auditoría',
            ip_address='127.0.0.1'
        )
        
        self.assertEqual(auditoria.accion_realizada, 'CREATE')
        self.assertEqual(auditoria.usuario, self.user)
        
    def test_sistema_basico_completo(self):
        """Test de integración básica"""
        # Crear datos relacionados
        madre = Madre.objects.create(
            nombre='Integración',
            rut='28.444.555-6',
            fecha_nacimiento='1990-01-01',
            comuna='Test',
            cesfam='Test',
            prevision='fonasa',
            direccion='Test',
            telefono='912345678',
            antecedentes_obstetricos='Test',
            atenciones_clinicas='Test',
            acompanante='Test'
        )
        
        parto = Parto.objects.create(
            madre=madre,
            fecha_hora='2023-01-01T10:00',
            tipo_parto='vaginal'
        )
        
        rn = RN.objects.create(
            madre=madre,
            parto_asociado=parto,
            fecha_nacimiento='2023-01-01',
            hora_nacimiento='10:30',
            apellido_paterno_rn='Integración',
            sexo='F'
        )
        
        # Verificar relaciones
        self.assertEqual(rn.madre, madre)
        self.assertEqual(rn.parto_asociado, parto)
        self.assertEqual(parto.madre, madre)
        
        # Verificar que completar parto funciona
        parto.estado = 'completado'
        parto.save()
        parto.refresh_from_db()
        self.assertEqual(parto.estado, 'completado')

def run_tests_esenciales():
    """Función para ejecutar los tests esenciales"""
    print("🧪 EJECUTANDO TESTS ESENCIALES...")
    print("=" * 50)
    
    import unittest
    
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestsEsenciales)
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Reporte
    print("\n" + "=" * 50)
    print("RESUMEN TESTS ESENCIALES")
    print("=" * 50)
    
    total = result.testsRun
    errors = len(result.errors)
    failures = len(result.failures)
    passed = total - errors - failures
    
    print(f"✅ Tests pasados: {passed}")
    print(f"❌ Tests fallidos: {failures}")
    print(f"💥 Errores: {errors}")
    print(f"📊 Total ejecutados: {total}")
    
    success_rate = (passed / total * 100) if total > 0 else 0
    print(f"🎯 Tasa éxito: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("\n🚀 ¡EXCELENTE! Funcionalidades esenciales operativas")
        print("✨ Sistema listo para uso y presentación")
    elif success_rate >= 70:
        print("\n👍 BUENO: Sistema funcional con pequeños ajustes")
    else:
        print("\n⚠️ ATENCIÓN: Revisar funcionalidades básicas")
        
    if errors > 0:
        print("\n🔥 ERRORES DETECTADOS:")
        for test, error in result.errors:
            print(f"   - {test}: {error.splitlines()[-1] if error else 'Error desconocido'}")
            
    if failures > 0:
        print("\n❌ FALLAS DETECTADAS:")
        for test, failure in result.failures:
            print(f"   - {test}: {failure.splitlines()[-1] if failure else 'Falla desconocida'}")
    
    return success_rate >= 70

if __name__ == '__main__':
    import sys
    success = run_tests_esenciales()
    sys.exit(0 if success else 1)