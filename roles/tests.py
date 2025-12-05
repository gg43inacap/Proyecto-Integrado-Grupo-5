
from django.test import TestCase
from .models import CustomUser

class CustomUserModelTest(TestCase):
	def test_create_user(self):
		user = CustomUser.objects.create(username='usuario', password='1234', role='ADMIN')
		self.assertEqual(user.username, 'usuario')
from django.test import TestCase

# Create your tests here.
