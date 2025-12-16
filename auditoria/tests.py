from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Auditoria
# pylint: disable=no-member

class AuditoriaViewsTest(TestCase):
	def setUp(self):
		User = get_user_model()
		self.user_auditor = User.objects.create_user(username='auditor', password='Inacap2025*', role='AUDITORIA')
		self.user_normal = User.objects.create_user(username='normal', password='Inacap2025*', role='SOME')
		self.log = Auditoria.objects.create(
			usuario=self.user_auditor,
			accion_realizada='LOGIN_SUCCESS',
			modelo_afectado='Usuario',
			registro_id=self.user_auditor.id,
			detalles_cambio='Login exitoso',
			ip_address='127.0.0.1'
		)

	def test_lista_auditorias_access(self):
		self.client.login(username='auditor', password='Inacap2025*')
		response = self.client.get(reverse('lista_auditorias'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Registros de Auditoría')

	def test_lista_auditorias_denied(self):
		self.client.login(username='normal', password='Inacap2025*')
		response = self.client.get(reverse('lista_auditorias'))
		self.assertEqual(response.status_code, 403)

	def test_detalle_auditoria_access(self):
		self.client.login(username='auditor', password='Inacap2025*')
		response = self.client.get(reverse('detalle_auditoria', args=[self.log.id]))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Detalle de Registro de Auditoría')

	def test_detalle_auditoria_denied(self):
		self.client.login(username='normal', password='Inacap2025*')
		response = self.client.get(reverse('detalle_auditoria', args=[self.log.id]))
		self.assertEqual(response.status_code, 403)

	def test_detalle_auditoria_not_found(self):
		self.client.login(username='auditor', password='Inacap2025*')
		response = self.client.get(reverse('detalle_auditoria', args=[9999]))
		self.assertEqual(response.status_code, 404)
