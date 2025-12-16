# Create your models here.
from django.contrib.auth.models import AbstractUser # Modelo base de usuario de Django
from django.db import models # Sistema de modelos de Django

ELEGIR_ROL = [ # Opciones de roles para los usuarios
    ('SOME', 'SOME'), # Rol de SOME
    ('MATRONA', 'Matrona'), # Rol de matrona
    ('SUPERVISOR', 'Supervisor'), # Rol de supervisor
    ('AUDITORIA', 'Auditoría'), # Rol de auditoría
    ('ADMIN', 'Administrador'), # Rol de administrador
]

class CustomUser(AbstractUser): # Usuario personalizado con campo 'role'
    role = models.CharField(max_length=20, choices=ELEGIR_ROL) # Rol del usuario, se elige de la lista ELEGIR_ROL
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True) # RUT chileno
    # Puedes agregar aquí otros campos si los necesitas (foto, etc.)

    def __str__(self): # Muestra el usuario como texto en el admin y otros lugares
        return f"{self.username} ({self.role})" # Ejemplo: juanperez (ADMIN)

