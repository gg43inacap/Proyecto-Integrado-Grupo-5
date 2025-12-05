# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

ELEGIR_ROL = [
    ('SOME', 'SOME'),
    ('MATRONA', 'Matrona'),
    ('SUPERVISOR', 'Supervisor'),
    ('AUDITORIA', 'Auditoría'),
    ('ADMIN', 'Administrador'),
]

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=ELEGIR_ROL)
    # Puedes agregar aquí otros campos si los necesitas (foto, etc.)

    def __str__(self):
        return f"{self.username} ({self.role})"
    
