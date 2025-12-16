from django.contrib import admin # Sistema de administración de Django
from .models import Parto, RN # Importa los modelos Parto y RN

admin.site.register(Parto) # Registra el modelo Parto en el panel de administración
admin.site.register(RN) # Registra el modelo RN en el panel de administración
