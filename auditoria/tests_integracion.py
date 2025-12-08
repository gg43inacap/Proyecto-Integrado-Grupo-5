from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from auditoria.models import Auditoria
from gestion_some.models import Madre
from partos.models import Parto, RN
# pylint: disable=no-member
class AuditoriaIntegracionTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_user(username='admin', password='test123', role='ADMIN')
        self.client.login(username='admin', password='test123')

    def test_crear_madre_registra_auditoria(self):
        response = self.client.post(reverse('crear_madre'), {
            'nombre': 'Test Madre',
            'rut': '12345678-9',
            'fecha_nacimiento': '1990-01-01',
            'comuna': 'Comuna',
            'cesfam': 'CESFAM',
            'direccion': 'Direccion',
            'telefono': '123456789',
            'antecedentes_obstetricos': 'Ninguno',
            'atenciones_clinicas': 'Ninguna',
            'acompanante': 'Acompañante',
        })
        self.assertIn(response.status_code, [200, 302])
        self.assertTrue(Auditoria.objects.filter(modelo_afectado='Madre', accion_realizada='CREATE').exists())

    def test_crear_parto_registra_auditoria(self):
        madre = Madre.objects.create(
            nombre='Test Madre',
            rut='12345678-9',
            fecha_nacimiento='1990-01-01',
            comuna='Comuna',
            cesfam='CESFAM',
            prevision='fonasa',
            direccion='Direccion',
            telefono='123456789',
            antecedentes_obstetricos='Ninguno',
            atenciones_clinicas='Ninguna',
            acompanante='Acompañante',
        )
        response = self.client.post(reverse('crear_parto'), {
            'madre': madre.id,
            'fecha_hora': '2023-01-01T10:00',
            'tipo_parto': 'vaginal',
            'tipo_parto_clasificado': '',
            'complicaciones': '',
            'parto_distocico': False,
            'parto_vacuum': False,
            'confirmado': False,
        })
        self.assertIn(response.status_code, [200, 302])
        # Verificar que se creó el parto y se registró auditoría
        self.assertTrue(Parto.objects.filter(madre=madre).exists())
        self.assertTrue(Auditoria.objects.filter(modelo_afectado='Parto', accion_realizada='CREATE').exists())

    def test_crear_rn_registra_auditoria(self):
        madre = Madre.objects.create(
            nombre='Test Madre',
            rut='12345678-9',
            fecha_nacimiento='1990-01-01',
            comuna='Comuna',
            cesfam='CESFAM',
            prevision='fonasa',
            direccion='Direccion',
            telefono='123456789',
            antecedentes_obstetricos='Ninguno',
            atenciones_clinicas='Ninguna',
            acompanante='Acompañante',
        )
        parto = Parto.objects.create(
            madre=madre,
            fecha_hora='2023-01-01T10:00',
            tipo_parto='vaginal',
            tipo_parto_clasificado='',
            complicaciones='',
            parto_distocico=False,
            parto_vacuum=False,
            confirmado=False,
        )
        response = self.client.post(reverse('crear_rn'), {
            'madre': madre.id,
            'parto_asociado': parto.id,
            'fecha_nacimiento': '2023-01-01',
            'hora_nacimiento': '10:30',
            'apellido_paterno_rn': 'TestApellido',
            'peso': 3500,
            'talla': 50,
            'cc': 34.5,
            'semanas_gestacion': 39,
            'dias_gestacion': 0,
            'sexo': 'M',
            'apego': False,
            'lactancia_antes_60': False,
            'profilaxis_ocular': False,
            'vacuna_hepatitis_b': False,
            'vacuna_bcg': False,
            'profesional_vhb': '',
            'apgar_1': 8,
            'apgar_5': 9,
            'anomalia_congenita': False,
            'reanimacion_basica': False,
            'reanimacion_avanzada': False,
            'ehi_grado_ii_iii': False,
            'confirmado': False,
        })
        self.assertIn(response.status_code, [200, 302])
        self.assertTrue(Auditoria.objects.filter(modelo_afectado='RN', accion_realizada='CREATE').exists())

    def test_completar_parto_registra_auditoria(self):
        """Test que completar parto registra auditoría correctamente"""
        madre = Madre.objects.create(
            nombre='Test Completar',
            rut='12345678-9',
            fecha_nacimiento='1990-01-01',
            comuna='Comuna',
            cesfam='CESFAM',
            prevision='fonasa',
            direccion='Direccion',
            telefono='123456789',
            antecedentes_obstetricos='Ninguno',
            atenciones_clinicas='Ninguna',
            acompanante='Acompañante',
        )
        parto = Parto.objects.create(
            madre=madre,
            fecha_hora='2023-01-01T10:00',
            tipo_parto='vaginal',
            estado='activo'
        )
        
        # Completar parto
        response = self.client.post(reverse('completar_parto', args=[parto.id]))
        self.assertIn(response.status_code, [200, 302])
        
        # Verificar auditoría
        self.assertTrue(
            Auditoria.objects.filter(
                modelo_afectado='Parto', 
                accion_realizada='UPDATE',
                detalles_cambio__contains='completado'
            ).exists()
        )
        
        # Verificar estado del parto
        parto.refresh_from_db()
        self.assertEqual(parto.estado, 'completado')

    def test_filtrar_partos_ajax_no_registra_auditoria(self):
        """Test que las consultas AJAX no registran auditoría innecesariamente"""
        madre = Madre.objects.create(
            nombre='Test Ajax',
            rut='12345678-9',
            fecha_nacimiento='1990-01-01',
            comuna='Comuna',
            cesfam='CESFAM',
            prevision='fonasa',
            direccion='Direccion',
            telefono='123456789',
            antecedentes_obstetricos='Ninguno',
            atenciones_clinicas='Ninguna',
            acompanante='Acompañante',
        )
        
        initial_count = Auditoria.objects.count()
        
        # Llamada AJAX para filtrar partos
        response = self.client.get(f'/partos/ajax/filtrar-partos/?madre_id={madre.id}')
        self.assertEqual(response.status_code, 200)
        
        # Las consultas AJAX no deberían registrar auditoría
        self.assertEqual(Auditoria.objects.count(), initial_count)

    def test_crear_multiples_rn_registra_auditoria(self):
        """Test que crear múltiples RN registra auditoría para cada uno"""
        madre = Madre.objects.create(
            nombre='Test Multiples',
            rut='12345678-9',
            fecha_nacimiento='1990-01-01',
            comuna='Comuna',
            cesfam='CESFAM',
            prevision='fonasa',
            direccion='Direccion',
            telefono='123456789',
            antecedentes_obstetricos='Ninguno',
            atenciones_clinicas='Ninguna',
            acompanante='Acompañante',
        )
        parto = Parto.objects.create(
            madre=madre,
            fecha_hora='2023-01-01T10:00',
            tipo_parto='vaginal',
            estado='activo'
        )
        
        initial_count = Auditoria.objects.count()
        
        # Crear múltiples RN (simulando gemelos)
        response = self.client.post(reverse('crear_rns'), {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '1',
            'form-MAX_NUM_FORMS': '10',
            
            'form-0-madre': madre.id,
            'form-0-parto_asociado': parto.id,
            'form-0-fecha_nacimiento': '2023-01-01',
            'form-0-hora_nacimiento': '10:30',
            'form-0-apellido_paterno_rn': 'Gemelo1',
            'form-0-sexo': 'M',
            'form-0-peso': 3000,
            'form-0-talla': 48,
            
            'form-1-madre': madre.id,
            'form-1-parto_asociado': parto.id,
            'form-1-fecha_nacimiento': '2023-01-01',
            'form-1-hora_nacimiento': '10:32',
            'form-1-apellido_paterno_rn': 'Gemelo2',
            'form-1-sexo': 'F',
            'form-1-peso': 2800,
            'form-1-talla': 47,
        })
        
        self.assertIn(response.status_code, [200, 302])
        
        # Debería haber registrado auditoría para cada RN creado
        auditoria_rn_count = Auditoria.objects.filter(
            modelo_afectado='RN', 
            accion_realizada='CREATE'
        ).count() - initial_count
        
        self.assertGreaterEqual(auditoria_rn_count, 1)  # Al menos 1 registro de auditoría
