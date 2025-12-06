from django.db import models # Sistema de modelos de Django


PREVISION_ELEGIR = [
    ('isapre', 'Isapre'),
    ('fonasa', 'Fonasa'),
    ('particular', 'Particular'),
]

class Madre(models.Model): # Modelo que representa a una madre
    nombre = models.CharField(max_length=100) # Nombre de la madre
    rut = models.CharField(max_length=12) # RUT de la madre
    fecha_nacimiento = models.DateField() # Fecha de nacimiento
    comuna = models.CharField(max_length=100) # Comuna de residencia
    cesfam = models.CharField(max_length=100) # CESFAM asociado
    prevision = models.CharField(max_length=20, choices=PREVISION_ELEGIR, default='fonasa') # Previsión de la madre
    direccion = models.CharField(max_length=200) # Dirección
    telefono = models.CharField(max_length=20) # Teléfono
    antecedentes_obstetricos = models.TextField() # Antecedentes obstétricos
    atenciones_clinicas = models.TextField() # Atenciones clínicas
    acompanante = models.CharField(max_length=100, blank=True, default="Sin Acompañante") # Nombre del acompañante

    def __str__(self): # Muestra la madre como texto
        return f"{self.nombre} ({self.rut})" # Ejemplo: Ana Pérez (12345678-9)

