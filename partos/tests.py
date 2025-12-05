# pylint: disable=no-member
from django.test import TestCase
from .models import Parto, RN
from gestion_some.models import Madre

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
			fecha_hora='2025-12-01T10:00:00Z',
			tipo_parto='vaginal',
			confirmado=True
		)
		self.assertEqual(str(parto), f"Parto {parto.pk} - {self.madre.nombre}")

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
			fecha_hora='2025-12-01T10:00:00Z',
			tipo_parto='vaginal',
			confirmado=True
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

