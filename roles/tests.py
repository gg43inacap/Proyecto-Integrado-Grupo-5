from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import CustomUser
from .utils import validar_rut
from auditoria.models import Auditoria
# pylint: disable=no-member

class CustomUserModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_user(username='admin', password='admin123', role='ADMIN', is_active=True)
        self.superadmin = User.objects.create_user(username='superadmin', password='super123', role='SUPERADMIN', is_active=True)
        self.normal = User.objects.create_user(username='normal', password='normal123', role='SOME', is_active=True)

    def test_create_user(self):
        user = CustomUser.objects.create(username='usuario', password='1234', role='ADMIN')
        self.assertEqual(user.username, 'usuario')
        
    def test_user_roles(self):
        # Test todos los roles disponibles
        roles = ['ADMIN', 'SOME', 'MATRONA', 'SUPERVISOR', 'AUDITORIA']
        for role in roles:
            user = CustomUser.objects.create_user(
                username=f'test_{role.lower()}',
                password='Inacap2025*',
                role=role,
                rut='8.168.483-9'
            )
            self.assertEqual(user.role, role)


        
class RutValidationTest(TestCase):
    def test_ruts_validos(self):
        ruts_validos = [
            '8.168.483-9',
            '12345678-5',
            '18765432-7',
            '16543210-K'
        ]
        for rut in ruts_validos:
            self.assertTrue(validar_rut(rut), f'RUT {rut} debería ser válido')
            
    def test_ruts_invalidos(self):
        ruts_invalidos = [
            '12345678-0',  # Dígito verificador incorrecto
            'abc123-4',    # Formato inválido
            '12345678',    # Sin dígito verificador
        ]
        for rut in ruts_invalidos:
            self.assertFalse(validar_rut(rut), f'RUT {rut} debería ser inválido')
            
class UserAuditoriaTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_user(username='admin_test', password='Inacap2025*', role='ADMIN')
        self.client = Client()
        self.client.login(username='admin_test', password='Inacap2025*')
        
    def test_crear_usuario_registra_auditoria(self):
        initial_count = Auditoria.objects.count()
        response = self.client.post(reverse('crear_usuario'), {
            'username': 'nuevo_usuario',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'role': 'SOME',
            'rut': '8.168.483-9',
            'is_active': True
        })
        # Verificar que se registró auditoría
        self.assertGreater(Auditoria.objects.count(), initial_count)

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

# Create your tests here.
