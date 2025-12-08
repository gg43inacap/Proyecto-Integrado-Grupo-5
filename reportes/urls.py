from . import views  # Importa las vistas de la aplicación reportes
from django.urls import path
  # Sistema de rutas de Django


app_name = 'reportes'


urlpatterns = [
    path('', views.lista_reportes, name='lista_reportes'),  # Ruta para listar reportes

    path("reporte_parto/", views.reporte_parto, name="reporte_parto"),
    path("reporte_nacidos_vivos/", views.reporte_nacidos_vivos, name="reporte_nacidos_vivos"),
    path("reporte_atencion_inmediata/", views.reporte_atencion_inmediata, name="reporte_atencion_inmediata"),


    path("roles/", views.panel_supervisor, name="panel_supervisor"),  # Ruta para el panel de supervisor
    path("componentes/selector_reportes/", views.selector_de_reportes, name="selector_reportes"),
    path("componentes/selector_filtros/", views.selector_de_filtros, name="selector_filtros"),
    path('exportar/', views.exportar_reporte, name='exportar_reporte'),  # Ruta para exportar reportes
]

## PLACEHOLDER - ACA SE TIENE QUE HACER FUNCIONAR EL EXPORTAR EXCEL Y LOS GRAFICOS