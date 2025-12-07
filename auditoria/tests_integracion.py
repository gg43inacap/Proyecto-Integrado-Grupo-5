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
        self.assertEqual(response.status_code, 302)
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
        self.assertEqual(response.status_code, 302)
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
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Auditoria.objects.filter(modelo_afectado='RN', accion_realizada='CREATE').exists())
