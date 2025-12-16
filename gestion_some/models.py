from django.db import models # Sistema de modelos de Django


PREVISION_ELEGIR = [
    ('isapre', 'Isapre'),
    ('fonasa', 'Fonasa'),
    ('particular', 'Particular'),
]


class Madre(models.Model): # Modelo que representa a una madre
    nombre = models.CharField(max_length=100) # Nombre de la madre
    rut = models.CharField(max_length=12, unique=True) # RUT de la madre, único
    fecha_nacimiento = models.DateField() # Fecha de nacimiento
    direccion = models.CharField(max_length=200) # Dirección
    comuna = models.CharField(max_length=100, help_text="Ej: Los Puelches") # Comuna de residencia
    telefono = models.CharField(max_length=20) # Teléfono
    cesfam = models.CharField(max_length=100) # CESFAM asociado
    prevision = models.CharField(max_length=20, choices=PREVISION_ELEGIR, default='fonasa') # Previsión de la madre
    migrante = models.BooleanField(default=False, choices=[(True, 'Sí'), (False, 'No')], help_text="¿Es migrante?") # Indica si es migrante
    pueblo_originario = models.BooleanField(default=False, choices=[(True, 'Sí'), (False, 'No')], help_text="¿Pertenece a pueblo originario?") # Indica si pertenece a pueblo originario
    antecedentes_obstetricos = models.TextField() # Antecedentes obstétricos
    alergias = models.BooleanField(default=False, help_text="¿Alergías a Comida/Medicamento?")
    alergias_si = models.TextField(max_length=100, blank=True, null=True, default="") #  Alergias


    def __str__(self): # Muestra la madre como texto
        return f"{self.nombre} ({self.rut})" # Ejemplo: Ana Pérez (12345678-9)

