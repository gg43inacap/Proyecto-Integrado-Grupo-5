from django.db import models

class Madre(models.Model):
    nombre = models.CharField(max_length=255)
    rut = models.CharField(max_length=12, unique=True)
    fecha_nacimiento = models.DateField()
    comuna = models.CharField(max_length=255, blank=True, null=True)
    cesfam = models.CharField(max_length=255, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    antecedentes_obstetricos = models.TextField(blank=True, null=True)
    atenciones_clinicas = models.TextField(blank=True, null=True)
    acompañante = models.CharField(max_length=255, blank=True, null=True)
    confirmado = models.BooleanField(default=False)  # Para control de Matrona
    objects = models.Manager()

    def __str__(self):
        return f"{self.nombre} ({self.rut})"

