from . import views, exportadores  # Importa las vistas de la aplicación reportes
from django.urls import path
  # Sistema de rutas de Django

urlpatterns = [
    path('', views.lista_reportes, name='lista_reportes'),  # Ruta para listar reportes
    path('crear/', views.crear_reporte, name='crear_reporte'),  # Ruta para crear reporte
    path('<int:reporte_id>/', views.detalle_reporte, name='detalle_reporte'),  # Ruta para ver detalles de reporte
    path('<int:reporte_id>/editar/', views.editar_reporte, name='editar_reporte'),  # Ruta para editar reporte
    path('<int:reporte_id>/eliminar/', views.eliminar_reporte, name='eliminar_reporte'), 
    path("reporte_parto/", views.reporte_parto, name="reporte_parto"),
    path("reporte_nacidos_vivos/", views.reporte_nacidos_vivos, name="reporte_nacidos_vivos"),
    path("reporte_atencion_inmediata/", views.reporte_atencion_inmediata, name="reporte_atencion_inmediata"),


  # Exportaciones Reporte 1
    path("exportar/reporte_parto/pdf/", exportadores.exportar_reporte_parto_pdf, name="exportar_reporte_parto_pdf"),
    path("exportar/reporte_parto/excel/", exportadores.exportar_reporte_parto_excel, name="exportar_reporte_parto_excel"),

    # Exportaciones Reporte 2
    path("exportar/reporte_nacidos_vivos/pdf/", exportadores.exportar_reporte_nacidos_vivos_pdf, name="exportar_reporte_nacidos_vivos_pdf"),
    path("exportar/reporte_nacidos_vivos/excel/", exportadores.exportar_reporte_nacidos_vivos_excel, name="exportar_reporte_nacidos_vivos_excel"),

    # Exportaciones Reporte 3
    path("exportar/reporte_atencion_inmediata/pdf/", exportadores.exportar_reporte_atencion_inmediata_pdf, name="exportar_reporte_atencion_inmediata_pdf"),
    path("exportar/reporte_atencion_inmediata/excel/", exportadores.exportar_reporte_atencion_inmediata_excel, name="exportar_reporte_atencion_inmediata_excel"),

    path("roles/", views.panel_supervisor, name="panel_supervisor"),  # Ruta para el panel de supervisor
    path("componentes/selector_reportes/", views.selector_de_reportes, name="selector_reportes"),
    path("componentes/selector_filtros/", views.selector_de_filtros, name="selector_filtros"),
]

## PLACEHOLDER - ACA SE TIENE QUE HACER FUNCIONAR EL EXPORTAR EXCEL Y LOS GRAFICOS