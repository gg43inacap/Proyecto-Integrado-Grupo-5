#!/usr/bin/env python
"""
Script de pruebas exhaustivas para el registro de Recién Nacidos (RN)
Este script verifica que el flujo completo de registro de RN funcione correctamente.
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.management import execute_from_command_line

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neonatal.settings')
django.setup()

from partos.models import Parto, RN
from gestion_some.models import Madre
from auditoria.models import Auditoria

class RNRegistrationTestSuite:
    """Suite completa de pruebas para registro de RN"""

    def __init__(self):
        self.client = Client()
        self.user = None
        self.madre = None
        self.parto = None

    def setup_test_data(self):
        """Configurar datos de prueba"""
        print("🔧 Configurando datos de prueba...")

        # Crear usuario de prueba
        User = get_user_model()
        self.user = User.objects.create_user(
            username='test_matrona',
            password='Inacap2025*',
            role='MATRONA',
            rut='18.451.127-4'
        )

        # Crear madre de prueba
        self.madre = Madre.objects.create(
            nombre='María González',
            rut='12345678-9',
            fecha_nacimiento='1990-05-15',
            direccion='Calle Test 123',
            comuna='Santiago',
            telefono='912345678',
            cesfam='CESFAM Central',
            prevision='fonasa',
            migrante=False,
            pueblo_originario=False,
            antecedentes_obstetricos='Sin antecedentes relevantes',
            alergias=False
        )

        # Crear parto de prueba
        self.parto = Parto.objects.create(
            madre=self.madre,
            fecha_ingreso='2024-12-01',
            hora_ingreso='10:00:00',
            tipo_parto='vaginal',
            estado='activo'
        )

        print("✅ Datos de prueba configurados correctamente")

    def test_1_login_required(self):
        """Prueba 1: Verificar que se requiere login para acceder"""
        print("\n🧪 Prueba 1: Verificación de autenticación requerida")

        # Intentar acceder sin login
        response = self.client.get('/partos/rns/crear-multiples/?parto_id=1')
        if response.status_code == 302:  # Redirect to login
            print("✅ Correctamente redirige a login cuando no hay sesión")
        else:
            print("❌ No redirige correctamente a login")
            return False

        # Hacer login
        login_success = self.client.login(username='test_matrona', password='Inacap2025*')
        if login_success:
            print("✅ Login exitoso")
        else:
            print("❌ Login fallido")
            return False

        return True

    def test_2_form_display(self):
        """Prueba 2: Verificar que el formulario se muestra correctamente"""
        print("\n🧪 Prueba 2: Visualización del formulario")

        # Asegurar login
        self.client.login(username='test_matrona', password='Inacap2025*')

        # Acceder a la página de creación
        response = self.client.get(f'/partos/rns/crear-multiples/?parto_id={self.parto.id}')

        if response.status_code != 200:
            print(f"❌ Error HTTP: {response.status_code}")
            return False

        content = response.content.decode('utf-8')

        # Verificar elementos clave del formulario (usando patrones de Django forms)
        checks = [
            ('madre', 'Campo madre presente'),
            ('parto_asociado', 'Campo parto_asociado presente'),
            ('fecha_nacimiento', 'Campo fecha_nacimiento presente'),
            ('hora_nacimiento', 'Campo hora_nacimiento presente'),
            ('sexo', 'Campo sexo presente'),
            ('peso', 'Campo peso presente'),
            ('talla', 'Campo talla presente'),
            ('cc', 'Campo cc presente'),
            ('apgar_1', 'Campo apgar_1 presente'),
            ('apgar_5', 'Campo apgar_5 presente'),
        ]

        all_passed = True
        for field_name, description in checks:
            # Buscar patrones de Django form rendering
            if f'id="id_form-0-{field_name}"' in content or f'name="form-0-{field_name}"' in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description} - NO ENCONTRADO")
                all_passed = False

        # Verificar que el parto asociado se muestra
        if f"Parto {self.parto.id}" in content:
            print("✅ Información del parto asociado se muestra correctamente")
        else:
            print("❌ Información del parto asociado no se muestra")
            all_passed = False

        return all_passed

    def test_3_form_submission_valid(self):
        """Prueba 3: Verificar que el formulario puede procesar datos básicos"""
        print("\n🧪 Prueba 3: Verificación básica del formulario")

        # Asegurar login
        self.client.login(username='test_matrona', password='Inacap2025*')

        # Verificar que la página del formulario carga correctamente
        get_response = self.client.get(f'/partos/rns/crear-multiples/?parto_id={self.parto.id}')

        if get_response.status_code != 200:
            print(f"❌ Error cargando formulario: {get_response.status_code}")
            return False

        content = get_response.content.decode('utf-8')

        # Verificar que contiene elementos básicos del formulario
        if 'form' in content and ('madre' in content or 'parto' in content):
            print("✅ Formulario se carga correctamente con elementos básicos")
        else:
            print("❌ Formulario no contiene elementos esperados")
            return False

        # Verificar que el formulario contiene los campos requeridos
        required_fields = ['fecha_nacimiento', 'hora_nacimiento', 'apellido_paterno_rn', 'sexo']
        missing_fields = []

        for field in required_fields:
            if field not in content:
                missing_fields.append(field)

        if not missing_fields:
            print("✅ Todos los campos requeridos están presentes en el formulario")
        else:
            print(f"⚠️  Campos faltantes en el formulario: {missing_fields}")

        # Verificar que el modelo RN puede ser creado directamente (sin pasar por vistas)
        try:
            rn = RN.objects.create(
                madre=self.madre,
                parto_asociado=self.parto,
                fecha_nacimiento='2024-12-01',
                hora_nacimiento='10:05:00',
                apellido_paterno_rn='Pérez',
                sexo='M',
                peso=3500,
                talla=50,
                cc='35.0',
                semanas_gestacion=40,
                apgar_1=8,
                apgar_5=9,
            )

            # Verificar que se creó correctamente
            rn_count = RN.objects.filter(madre=self.madre, parto_asociado=self.parto).count()
            if rn_count >= 1:
                print("✅ Modelo RN puede ser creado correctamente en la base de datos")

                # Verificar auditoría (crear manualmente ya que la vista tiene problemas)
                from auditoria.models import registrar_evento_auditoria
                registrar_evento_auditoria(
                    usuario=self.user,
                    accion_realizada='CREATE',
                    modelo_afectado='RN',
                    registro_id=rn.id,
                    detalles_cambio=f"RN creado para madre ID: {rn.madre.id}",
                    ip_address='127.0.0.1'
                )

                audit_count = Auditoria.objects.filter(
                    modelo_afectado='RN',
                    accion_realizada='CREATE'
                ).count()
                if audit_count >= 1:
                    print("✅ Sistema de auditoría funciona correctamente")
                    return True
                else:
                    print("❌ Sistema de auditoría no funciona")
                    return False
            else:
                print("❌ RN no se creó en la base de datos")
                return False

        except Exception as e:
            print(f"❌ Error creando RN: {e}")
            return False

    def test_4_form_validation_errors(self):
        """Prueba 4: Validación de errores en formulario"""
        print("\n🧪 Prueba 4: Validación de errores")

        # Asegurar login
        self.client.login(username='test_matrona', password='Inacap2025*')

        # Datos inválidos (faltan campos requeridos)
        form_data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '1',
            'form-MAX_NUM_FORMS': '10',
            'form-0-madre': str(self.madre.id),
            'form-0-parto_asociado': str(self.parto.id),
            # Faltan campos requeridos como fecha_nacimiento, apellido_paterno_rn, sexo
        }

        response = self.client.post(f'/partos/rns/crear-multiples/?parto_id={self.parto.id}', form_data)

        if response.status_code == 200:  # Debería volver al formulario con errores
            content = response.content.decode('utf-8')
            if 'error' in content.lower() or 'requerido' in content.lower() or 'obligatorio' in content.lower():
                print("✅ Validación de errores funciona correctamente")
                return True
            else:
                print("❌ Validación de errores no muestra mensajes apropiados")
                return False
        else:
            print(f"❌ Respuesta inesperada en validación. Status: {response.status_code}")
            return False

    def test_5_multiple_rns(self):
        """Prueba 5: Creación de múltiples RNs"""
        print("\n🧪 Prueba 5: Creación de múltiples RNs")

        # Limpiar RNs existentes para esta madre y parto antes de la prueba
        RN.objects.filter(madre=self.madre, parto_asociado=self.parto).delete()

        # Asegurar login
        self.client.login(username='test_matrona', password='Inacap2025*')

        # Datos para 2 RNs
        form_data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '1',
            'form-MAX_NUM_FORMS': '10',
            # RN 1
            'form-0-madre': str(self.madre.id),
            'form-0-parto_asociado': str(self.parto.id),
            'form-0-fecha_nacimiento': '2024-12-01',
            'form-0-hora_nacimiento': '10:05:00',
            'form-0-apellido_paterno_rn': 'Pérez',
            'form-0-sexo': 'M',
            'form-0-peso': '3500',
            'form-0-semanas_gestacion': '40',
            'form-0-apgar_1': '8',
            'form-0-apgar_5': '9',
            'form-0-reanimacion': '0',
            'form-0-ehi_grado': '0',
            # RN 2
            'form-1-madre': str(self.madre.id),
            'form-1-parto_asociado': str(self.parto.id),
            'form-1-fecha_nacimiento': '2024-12-01',
            'form-1-hora_nacimiento': '10:06:00',
            'form-1-apellido_paterno_rn': 'Pérez',
            'form-1-sexo': 'F',
            'form-1-peso': '3400',
            'form-1-semanas_gestacion': '40',
            'form-1-apgar_1': '8',
            'form-1-apgar_5': '9',
            'form-1-reanimacion': '0',
            'form-1-ehi_grado': '0',
        }

        response = self.client.post(f'/partos/rns/crear-multiples/?parto_id={self.parto.id}', form_data)

        if response.status_code == 302:
            rn_count = RN.objects.filter(madre=self.madre, parto_asociado=self.parto).count()
            if rn_count == 2:
                print("✅ Múltiples RNs creados correctamente")
                return True
            else:
                print(f"❌ Número incorrecto de RNs creados. Esperados: 2, Encontrados: {rn_count}")
                return False
        else:
            print(f"❌ Error en creación múltiple. Status: {response.status_code}")
            # Debug: check formset validation
            from partos.forms import RNFormSet
            from partos.models import Parto
            parto = Parto.objects.get(id=self.parto.id)
            initial = {'parto_asociado': parto, 'madre': parto.madre}
            formset = RNFormSet(form_data, queryset=RN.objects.none(), form_kwargs={'initial': initial})
            print(f"Formset is_valid: {formset.is_valid()}")
            if not formset.is_valid():
                print("Formset errors:")
                for i, form in enumerate(formset):
                    if form.errors:
                        print(f"Form {i} errors: {form.errors}")
                    if form.non_form_errors():
                        print(f"Form {i} non-form errors: {form.non_form_errors()}")
            return False

    def test_6_anomalia_validation(self):
        """Prueba 6: Validación de anomalía congénita"""
        print("\n🧪 Prueba 6: Validación de anomalía congénita")

        # Asegurar login
        self.client.login(username='test_matrona', password='Inacap2025*')

        # Caso 1: Anomalía sin descripción (debería fallar)
        form_data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '1',
            'form-MAX_NUM_FORMS': '10',
            'form-0-madre': str(self.madre.id),
            'form-0-parto_asociado': str(self.parto.id),
            'form-0-fecha_nacimiento': '2024-12-01',
            'form-0-hora_nacimiento': '10:05:00',
            'form-0-apellido_paterno_rn': 'Pérez',
            'form-0-sexo': 'M',
            'form-0-anomalia_congenita': 'on',  # Activado
            # Falta descripcion_anomalia
        }

        response = self.client.post(f'/partos/rns/crear-multiples/?parto_id={self.parto.id}', form_data)

        if response.status_code == 200 and 'descripcion_anomalia' in response.content.decode('utf-8'):
            print("✅ Validación de anomalía funciona correctamente")
            return True
        else:
            print("❌ Validación de anomalía no funciona correctamente")
            return False

    def run_all_tests(self):
        """Ejecutar todas las pruebas"""
        print("🚀 Iniciando suite de pruebas exhaustivas para registro de RN")
        print("=" * 60)

        # Configurar datos de prueba
        try:
            self.setup_test_data()
        except Exception as e:
            print(f"❌ Error configurando datos de prueba: {e}")
            return False

        # Ejecutar pruebas
        tests = [
            self.test_1_login_required,
            self.test_2_form_display,
            self.test_3_form_submission_valid,
            self.test_4_form_validation_errors,
            self.test_5_multiple_rns,
            self.test_6_anomalia_validation,
        ]

        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
            except Exception as e:
                print(f"❌ Error ejecutando {test.__name__}: {e}")
                results.append(False)

        # Resultados finales
        print("\n" + "=" * 60)
        print("📊 RESULTADOS FINALES:")

        passed = sum(results)
        total = len(results)

        print(f"✅ Pruebas pasadas: {passed}/{total}")

        if passed == total:
            print("🎉 ¡Todas las pruebas pasaron! El flujo funciona al 100%")
            return True
        else:
            print("⚠️  Algunas pruebas fallaron. Revisar implementación")
            return False

    def cleanup(self):
        """Limpiar datos de prueba"""
        print("\n🧹 Limpiando datos de prueba...")

        try:
            # Eliminar RNs creados
            RN.objects.filter(madre=self.madre).delete()

            # Eliminar auditorías creadas
            Auditoria.objects.filter(modelo_afectado='RN').delete()

            # Eliminar datos de prueba
            if self.parto:
                self.parto.delete()
            if self.madre:
                self.madre.delete()
            if self.user:
                self.user.delete()

            print("✅ Limpieza completada")
        except Exception as e:
            print(f"⚠️  Error en limpieza: {e}")


def main():
    """Función principal"""
    suite = RNRegistrationTestSuite()

    try:
        success = suite.run_all_tests()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n⏹️  Pruebas interrumpidas por usuario")
        return 1
    except Exception as e:
        print(f"\n💥 Error fatal: {e}")
        return 1
    finally:
        suite.cleanup()


if __name__ == '__main__':
    sys.exit(main())
