from django.test import TestCase, Client
from django.urls import reverse
from roles.models import CustomUser
from roles.utils import validar_rut

class LoginTestCase(TestCase):
	def setUp(self):
		self.client = Client()
		self.username = 'testuser'
		self.password = 'testpass123'
		self.rut = '8.168.483-9'  # RUT válido
		self.user = CustomUser.objects.create_user(username=self.username, password=self.password, rut=self.rut)

	def test_login_with_username(self):
		response = self.client.post(reverse('login'), {
			'login_type': 'username',
			'username': self.username,
			'password': self.password
		})
		self.assertEqual(response.status_code, 302)  # Redirige a inicio
		self.assertTrue('_auth_user_id' in self.client.session)

	def test_login_with_rut(self):
		response = self.client.post(reverse('login'), {
			'login_type': 'rut',
			'username': self.rut,
			'password': self.password
		})
		self.assertEqual(response.status_code, 302)
		self.assertTrue('_auth_user_id' in self.client.session)

	def test_rut_validator(self):
			rut_valido = '8.168.483-9'  # Compatible con el algoritmo
			rut_valido_simple = '81684839'
			rut_valido_2 = '19.058.317-1'
			rut_valido_2_simple = '190583171'
			rut_invalido = '8.168.483-1'
			# Prueba con formato y sin formato
			self.assertTrue(validar_rut(rut_valido))
			self.assertTrue(validar_rut(rut_valido_simple))
			self.assertTrue(validar_rut(rut_valido_2))
			self.assertTrue(validar_rut(rut_valido_2_simple))
			self.assertFalse(validar_rut(rut_invalido))
			# Prueba con formato y sin formato
			self.assertTrue(validar_rut(rut_valido))
			self.assertTrue(validar_rut(rut_valido_simple))
			self.assertFalse(validar_rut(rut_invalido))
