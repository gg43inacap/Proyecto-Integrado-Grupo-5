from . import views  # Importa las vistas de la aplicación reportes
from django.urls import path  # Sistema de rutas de Django

urlpatterns = [
    path('', views.lista_reportes, name='lista_reportes'),  # Ruta para listar reportes
    path('crear/', views.crear_reporte, name='crear_reporte'),  # Ruta para crear reporte
    path('<int:reporte_id>/', views.detalle_reporte, name='detalle_reporte'),  # Ruta para ver detalles de reporte
    path('<int:reporte_id>/editar/', views.editar_reporte, name='editar_reporte'),  # Ruta para editar reporte
    path('<int:reporte_id>/eliminar/', views.eliminar_reporte, name='eliminar_reporte'),  # Ruta para eliminar reporte
    path('dashboard/', views.lista_reportes, name='reportes_dashboard'),  # Añadida para compatibilidad con panel supervisor
]

## PLACEHOLDER - ACA SE TIENE QUE HACER FUNCIONAR EL EXPORTAR EXCEL Y LOS GRAFICOS