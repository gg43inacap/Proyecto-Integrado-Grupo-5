# pylint: disable=no-member
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Parto, RN
from gestion_some.models import Madre
from auditoria.models import Auditoria
import json


class PartoModelTest(TestCase):
    def setUp(self):
        self.madre = Madre.objects.create(
            nombre='Juana', rut='12345678-9', fecha_nacimiento='1990-01-01',
            comuna='Santiago', cesfam='CESFAM Central', direccion='Calle Falsa 123',
            telefono='912345678', antecedentes_obstetricos='Ninguno',
            atenciones_clinicas='Ninguna', acompanante='Pedro'
        )

    def test_create_parto(self):
        parto = Parto.objects.create(
            madre=self.madre,
            fecha_ingreso= '2023-01-01',
            hora_ingreso= '10:00',
            tipo_parto='vaginal',
            confirmado=True
        )
        self.assertEqual(str(parto), f"Parto {parto.pk} - {self.madre.nombre}")
        # Test estado por defecto
        self.assertEqual(parto.estado, 'activo')
        
    def test_completar_parto(self):
        parto = Parto.objects.create(
            madre=self.madre,
            fecha_ingreso= '2023-01-01',
            hora_ingreso= '10:00',
            tipo_parto='vaginal',
            estado='activo'
        )
        parto.estado = 'completado'
        parto.save()
        self.assertEqual(parto.estado, 'completado')

class RNModelTest(TestCase):
    def setUp(self):
        self.madre = Madre.objects.create(
            nombre='Juana', rut='12345678-9', fecha_nacimiento='1990-01-01',
            comuna='Santiago', cesfam='CESFAM Central', direccion='Calle Falsa 123',
            telefono='912345678', antecedentes_obstetricos='Ninguno',
            atenciones_clinicas='Ninguna', acompanante='Pedro'
        )
        self.parto = Parto.objects.create(
            madre=self.madre,
            fecha_ingreso= '2023-01-01',
            hora_ingreso= '10:00',
            tipo_parto='vaginal',
            confirmado=True,
            estado='activo'
        )

    def test_create_rn(self):
        rn = RN.objects.create(
            madre=self.madre,
            parto_asociado=self.parto,
            fecha_nacimiento='2025-12-01',
            hora_nacimiento='10:05:00',
            apellido_paterno_rn='González',
            sexo='M'
        )
        self.assertEqual(rn.apellido_paterno_rn, 'González')
        

class PartoAjaxTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='test', password='Inacap2025*', role='MATRONA')
        self.client = Client()
        self.client.login(username='test', password='Inacap2025*')
        
        self.madre = Madre.objects.create(
            nombre='Test Madre', rut='12345678-9', fecha_nacimiento='1990-01-01',
            comuna='Santiago', cesfam='CESFAM Central', direccion='Calle Test',
            telefono='912345678', antecedentes_obstetricos='Ninguno',
            atenciones_clinicas='Ninguna', acompanante='Test'
        )
        
        self.parto_activo = Parto.objects.create(
            madre=self.madre,
            fecha_ingreso= '2023-01-01',
            hora_ingreso= '10:00',
            tipo_parto='vaginal',
            estado='activo'
        )
        
        self.parto_completado = Parto.objects.create(
            madre=self.madre,
            fecha_ingreso= '2023-01-01',
            hora_ingreso= '10:00',
            tipo_parto='cesarea',
            estado='completado'
        )
    
    def test_filtrar_partos_ajax(self):
        response = self.client.get(f'/partos/ajax/filtrar-partos/?madre_id={self.madre.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        # Solo debe devolver partos activos
        self.assertEqual(len(data['partos']), 1)
        self.assertEqual(data['partos'][0]['id'], self.parto_activo.id)

