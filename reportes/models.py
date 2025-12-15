from django.db import models
from django.utils import timezone

# Importas otros modelos si quieres relacionarlos
from partos.models import Parto, RN
from gestion_some.models import Madre

class Reporte(models.Model):
    TIPOS_CHOICES = [
        ('REM A24', 'REM A24'),
        ('REM A02', 'REM A02'),
        ('REM A10', 'REM A10'),
    ]

    tipo = models.CharField(max_length=50, choices=TIPOS_CHOICES)
    fecha = models.DateTimeField(default=timezone.now)
    descripcion = models.TextField(blank=True, null=True)

    # Relación opcional con Madre, Parto o RN si quieres vincular el reporte
    madre = models.ForeignKey(Madre, on_delete=models.SET_NULL, null=True, blank=True)
    parto = models.ForeignKey(Parto, on_delete=models.SET_NULL, null=True, blank=True)
    rn = models.ForeignKey(RN, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.tipo} - {self.fecha.date()}"