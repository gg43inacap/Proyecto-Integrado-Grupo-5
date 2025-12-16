from django.db import models # Sistema de modelos de Django
from gestion_some.models import Madre # Importa el modelo Madre
from django.utils import timezone


class Parto(models.Model): # Modelo que representa un parto
    TIPO_PARTO_CHOICES = [
        ('vaginal', 'Vaginal'),
        ('cesarea_electiva', 'Cesárea Electiva'),
        ('instrumental', 'Instrumental'),
        ('cesarea_urgencia', 'Cesárea de Urgencia'),
    ]
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('completado', 'Completado'),
    ]
    madre = models.ForeignKey(Madre, on_delete=models.CASCADE, related_name='partos') # Relación con la madre
    #fecha_hora = models.DateTimeField() # Fecha y hora del parto
    fecha_ingreso = models.DateField(help_text="Fecha de ingreso de la madre al evento", null=True, blank=True)
    hora_ingreso = models.TimeField(help_text="Hora de ingreso de la madre al evento", null=True, blank=True)
    tipo_parto = models.CharField(max_length=20, choices=TIPO_PARTO_CHOICES) # Tipo de parto
    complicaciones = models.TextField(blank=True, null=True) # Complicaciones durante el parto
    parto_distocico = models.BooleanField(default=False) # Indica si el parto fue distócico
    parto_vacuum = models.BooleanField(default=False) # Indica si se usó vacuum en el parto
    tiene_acompanante = models.BooleanField(default=False, help_text="¿Tiene acompañante?")
    nombre_acompanante = models.CharField(max_length=100, blank=True, null=True, default="") # Nombre del acompañante si corresponde
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo') # Estado del parto
    objects = models.Manager()

    def __str__(self):
        return f"Parto {self.pk} - {self.madre.nombre if hasattr(self.madre, 'nombre') else self.madre}"

# En Parto
def es_cesarea_electiva(self):
    return self.tipo_parto == 'cesarea_electiva'

def es_cesarea_urgencia(self):
    return self.tipo_parto == 'cesarea_urgencia'

# En RN
def apgar_bajo_minuto(self):
    return self.apgar_1 is not None and self.apgar_1 <= 3

def apgar_bajo_5min(self):
    return self.apgar_5 is not None and self.apgar_5 <= 6


class RN(models.Model): # Modelo que representa un recién nacido
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('I', 'Indeterminado'),
    ]
    
    EHI_GRADO_CHOICES = [
        (0, 'Sin EHI'),
        (1, 'EHI Grado I (Leve)'),
        (2, 'EHI Grado II (Moderado)'),
        (3, 'EHI Grado III (Severo)'),
    ]
    
    REANIMACION_CHOICES = [
        (0, 'Sin reanimación'),
        (1, 'Reanimación básica'),
        (2, 'Reanimación avanzada'),
    ]
    
    fecha_nacimiento = models.DateField() # Fecha de nacimiento
    hora_nacimiento = models.TimeField() # Hora de nacimiento
    apellido_paterno_rn = models.CharField(max_length=255) # Apellido paterno del recién nacido
    peso = models.IntegerField(blank=True, null=True) # Peso al nacer
    talla = models.IntegerField(blank=True, null=True) # Talla al nacer
    cc = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True) # Circunferencia cefálica
    semanas_gestacion = models.IntegerField(blank=True, null=True) # Semanas de gestación
    dias_gestacion = models.IntegerField(blank=True, null=True) # Días de gestación
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES) # Sexo del recién nacido
    apego = models.BooleanField(default=False) # Indica si hubo apego
    lactancia_antes_60 = models.BooleanField(default=False) # Indica si hubo lactancia antes de las 60 minutos
    profilaxis_ocular = models.BooleanField(default=False) # Indica si se realizó profilaxis ocular
    vacuna_hepatitis_b = models.BooleanField(default=False) # Indica si se administró vacuna hepatitis B
    vacuna_bcg = models.BooleanField(default=False) # Indica si se administró vacuna BCG
    profesional_vhb = models.CharField(max_length=255, blank=True, null=True) # Profesional que administró VHB
    apgar_1 = models.IntegerField(blank=True, null=True) # Puntaje de Apgar a 1 minuto
    apgar_5 = models.IntegerField(blank=True, null=True) # Puntaje de Apgar a 5 minutos
    anomalia_congenita = models.BooleanField(default=False) # Indica si hay anomalía congénita
    descripcion_anomalia = models.CharField(max_length=255, blank=True, null=True, default="") # Descripción de la anomalía congénita si corresponde
    reanimacion = models.IntegerField(choices=REANIMACION_CHOICES, default=0) # Nivel de reanimación requerida (0-2)
    ehi_grado = models.IntegerField(choices=EHI_GRADO_CHOICES, default=0) # Grado de Encefalopatía Hipóxico-Isquémica (0-3)
    objects = models.Manager()

    def clean(self):
        """Validación personalizada del modelo"""
        from django.core.exceptions import ValidationError
        
        # Si tiene anomalía congénita, debe tener descripción
        if self.anomalia_congenita and not self.descripcion_anomalia:
            raise ValidationError({
                'descripcion_anomalia': 'Debe describir la anomalía congénita.'
            })
        
        # Si no tiene anomalía, limpiar la descripción
        if not self.anomalia_congenita:
            self.descripcion_anomalia = ''

    def save(self, *args, **kwargs):
        """Sobrescribir save para ejecutar validación"""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.apellido_paterno_rn} - {self.madre.nombre if hasattr(self.madre, 'nombre') else self.madre}"
