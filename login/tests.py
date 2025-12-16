from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from roles.models import CustomUser
from roles.utils import validar_rut
from auditoria.models import Auditoria
# pylint: disable=no-member

class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpass123'
        self.rut = '8.168.483-9'  # RUT válido
        self.user = CustomUser.objects.create_user(
            username=self.username, 
            password=self.password, 
            rut=self.rut,
            role='SOME'
        )

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
        
    def test_login_dual_functionality(self):
        # Test que ambos métodos funcionen para usuarios demo
        User = get_user_model()
        demo_user = User.objects.create_user(
            username='demo_test',
            password='demo123', 
            rut='12345678-5',
            role='MATRONA'
        )
        
        # Login con username
        response1 = self.client.post(reverse('login'), {
            'login_type': 'username',
            'username': 'demo_test',
            'password': 'demo123'
        })
        self.assertEqual(response1.status_code, 302)
        self.client.logout()
        
        # Login con RUT
        response2 = self.client.post(reverse('login'), {
            'login_type': 'rut',
            'username': '12345678-5',
            'password': 'demo123'
        })
        self.assertEqual(response2.status_code, 302)
        
    def test_login_failure(self):
        response = self.client.post(reverse('login'), {
            'login_type': 'username',
            'username': 'wrong_user',
            'password': 'wrong_pass'
        })
        self.assertEqual(response.status_code, 200)  # Permanece en login
        self.assertFalse('_auth_user_id' in self.client.session)
        
    def test_rut_validation_in_login(self):
        # Test validación de formato RUT
        invalid_ruts = ['123', 'abc-1', '00000000-0']
        for invalid_rut in invalid_ruts:
            response = self.client.post(reverse('login'), {
                'login_type': 'rut',
                'username': invalid_rut,
                'password': 'anypass'
            })
            self.assertEqual(response.status_code, 200)
            self.assertFalse('_auth_user_id' in self.client.session)

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
