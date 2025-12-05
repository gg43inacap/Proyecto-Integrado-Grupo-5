# pylint: disable=no-member
from django.test import TestCase
from .models import Madre

class MadreModelTest(TestCase):
	def test_create_madre(self):
		madre = Madre.objects.create(
			nombre='Juana', rut='12345678-9', fecha_nacimiento='1990-01-01',
			comuna='Santiago', cesfam='CESFAM Central', direccion='Calle Falsa 123',
			telefono='912345678', antecedentes_obstetricos='Ninguno',
			atenciones_clinicas='Ninguna', acompanante='Pedro'
		)
		self.assertEqual(madre.nombre, 'Juana')
from django.test import TestCase

# Create your tests here.
