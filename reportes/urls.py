from . import views  # Importa las vistas de la aplicación reportes
from . import exportadores  # Importa las funciones de exportación
from django.urls import path
  # Sistema de rutas de Django


app_name = 'reportes'


urlpatterns = [
    path("exportar/rem_a24/excel/", views.exportar_rem_a24_excel, name="exportar_rem_a24_excel"),
    path("exportar/rem_a24/pdf/", views.exportar_rem_a24_pdf, name="exportar_rem_a24_pdf"),
    path("rem_24/", views.rem_24, name="rem_24"), 
]

