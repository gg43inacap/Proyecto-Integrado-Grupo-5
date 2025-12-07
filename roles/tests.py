
from django.test import TestCase
from .models import CustomUser

from django.urls import reverse
from django.contrib.auth import get_user_model

class CustomUserModelTest(TestCase):
	def setUp(self):
		User = get_user_model()
		self.admin = User.objects.create_user(username='admin', password='admin123', role='ADMIN', is_active=True)
		self.superadmin = User.objects.create_user(username='superadmin', password='super123', role='SUPERADMIN', is_active=True)
		self.normal = User.objects.create_user(username='normal', password='normal123', role='SOME', is_active=True)

	def test_create_user(self):
		user = CustomUser.objects.create(username='usuario', password='1234', role='ADMIN')
		self.assertEqual(user.username, 'usuario')

	def test_admin_cannot_edit_superadmin(self):
		self.client.login(username='admin', password='admin123')
		url = reverse('editar_usuario', args=[self.superadmin.pk])
		response = self.client.get(url)
		self.assertRedirects(response, reverse('lista_usuarios'))

	def test_admin_cannot_block_superadmin(self):
		self.client.login(username='admin', password='admin123')
		url = reverse('bloquear_usuario', args=[self.superadmin.pk])
		response = self.client.post(url)
		self.superadmin.refresh_from_db()
		self.assertTrue(self.superadmin.is_active)

	def test_admin_can_block_normal_user(self):
		self.client.login(username='admin', password='admin123')
		url = reverse('bloquear_usuario', args=[self.normal.pk])
		response = self.client.post(url)
		self.normal.refresh_from_db()
		self.assertFalse(self.normal.is_active)

	def test_admin_can_edit_normal_user(self):
		self.client.login(username='admin', password='admin123')
		url = reverse('editar_usuario', args=[self.normal.pk])
		response = self.client.post(url, {'username': 'normal', 'role': 'SOME', 'is_active': True, 'is_staff': False})
		self.normal.refresh_from_db()
		self.assertEqual(self.normal.username, 'normal')
from django.test import TestCase

# Create your tests here.
