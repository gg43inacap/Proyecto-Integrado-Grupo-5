from django.db import models # Sistema de modelos de Django

# Aquí puedes definir el modelo para los reportes
# Ejemplo:
# class Reporte(models.Model): # Modelo para un reporte
#     campo1 = models.CharField(max_length=100) # Campo de texto
#     campo2 = models.DateField() # Campo de fecha
#     ...

from partos.models import Parto, RN
from gestion_some.models import Madre
# Create your models here.
