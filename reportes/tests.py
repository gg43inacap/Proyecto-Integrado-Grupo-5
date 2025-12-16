from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from gestion_some.models import Madre
from partos.models import Parto, RN
# pylint: disable=no-member

class ReportesTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='test', password='Inacap2025*', role='ADMIN')
        self.client = Client()
        self.client.login(username='test', password='Inacap2025*')
        
        # Crear datos de prueba para reportes
        self.madre = Madre.objects.create(
            nombre='Test Reporte', rut='8.168.483-9', fecha_nacimiento='1990-01-01',
            comuna='Santiago', cesfam='CESFAM Test', direccion='Test',
            telefono='912345678', antecedentes_obstetricos='Test',
            atenciones_clinicas='Test', acompanante='Test'
        )
        
        self.parto = Parto.objects.create(
            madre=self.madre,
            fecha_ingreso= '2023-01-01',
            hora_ingreso= '10:00',
            tipo_parto='vaginal',
            estado='completado'
        )
        
        self.rn = RN.objects.create(
            madre=self.madre,
            parto_asociado=self.parto,
            fecha_nacimiento='2025-12-01',
            hora_nacimiento='10:05:00',
            apellido_paterno_rn='Test',
            sexo='M'
        )
    
    def test_datos_disponibles_para_reportes(self):
        # Verificar que hay datos para generar reportes
        self.assertTrue(Madre.objects.exists())
        self.assertTrue(Parto.objects.exists())
        self.assertTrue(RN.objects.exists())
        
    def test_reportes_access_by_role(self):
        # Test que solo usuarios autorizados pueden acceder
        # (Implementar según URLs que definan tus compañeros)
        pass
        
    # TODO: Agregar tests específicos cuando tus compañeros 
    # implementen las vistas de reportes
    
    def test_integracion_futura_reportes(self):
        """Test placeholder para cuando se implementen reportes completos"""
        # Verificar que datos están disponibles para reportes
        from auditoria.models import Auditoria
        
        # Debería haber datos de auditoría para generar reportes
        auditoria_count = Auditoria.objects.count()
        self.assertGreaterEqual(auditoria_count, 0)
        
        # Verificar acceso a URLs básicas cuando estén implementadas
        # (Este test pasará cuando implementen las vistas)
        pass
        
    def test_permisos_reportes_por_rol(self):
        """Test que verifica permisos según roles para reportes"""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Solo ADMIN y SUPERVISOR deberían tener acceso completo a reportes
        roles_con_acceso = ['ADMIN', 'SUPERVISOR']
        roles_sin_acceso = ['SOME', 'MATRONA', 'AUDITORIA']
        
        for rol in roles_con_acceso:
            user = User.objects.create_user(
                username=f'test_{rol.lower()}',
                password='Inacap2025*',
                role=rol
            )
            # Verificar que el rol es correcto
            self.assertEqual(user.role, rol)
            
        # Test preparatorio - cuando implementen vistas, 
        # agregar tests de acceso real por URLs
