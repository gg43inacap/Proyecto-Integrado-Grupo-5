from . import views  # Importa las vistas de la aplicación reportes
from . import exportadores  # Importa las funciones de exportación
from django.urls import path
  # Sistema de rutas de Django


app_name = 'reportes'


urlpatterns = [
    path('', views.selector_de_reportes, name='lista_reportes'),  # Ruta principal que muestra selector de reportes
    path('dashboard/', views.selector_de_reportes, name='reportes_dashboard'),  # Dashboard de reportes para supervisor

    path("reporte_parto/", views.reporte_parto, name="reporte_parto"),
    path("reporte_nacidos_vivos/", views.reporte_nacidos_vivos, name="reporte_nacidos_vivos"),
    path("reporte_atencion_inmediata/", views.reporte_atencion_inmediata, name="reporte_atencion_inmediata"),


    path("roles/", views.panel_supervisor, name="panel_supervisor"),  # Ruta para el panel de supervisor
    path("componentes/selector_reportes/", views.selector_de_reportes, name="selector_reportes"),
    path("componentes/selector_filtros/", views.selector_de_filtros, name="selector_filtros"),
    path('exportar/', views.exportar_reporte, name='exportar_reporte'),  # Ruta para exportar reportes
    
    # URLs para exportación de reportes específicos
    # Reporte de Partos
    path('exportar/parto/pdf/', exportadores.exportar_reporte_parto_pdf, name='exportar_parto_pdf'),
    path('exportar/parto/excel/', exportadores.exportar_reporte_parto_excel, name='exportar_parto_excel'),
    
    # Reporte de Nacidos Vivos
    path('exportar/nacidos_vivos/pdf/', exportadores.exportar_reporte_nacidos_vivos_pdf, name='exportar_nacidos_vivos_pdf'),
    path('exportar/nacidos_vivos/excel/', exportadores.exportar_reporte_nacidos_vivos_excel, name='exportar_nacidos_vivos_excel'),
    
    # Reporte de Atención Inmediata
    path('exportar/atencion_inmediata/pdf/', exportadores.exportar_reporte_atencion_inmediata_pdf, name='exportar_atencion_inmediata_pdf'),
    path('exportar/atencion_inmediata/excel/', exportadores.exportar_reporte_atencion_inmediata_excel, name='exportar_atencion_inmediata_excel'),
]