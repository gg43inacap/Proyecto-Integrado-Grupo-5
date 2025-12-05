from . import views
from django.urls import path

urlpatterns = [
    path('', views.lista_reportes, name='lista_reportes'),
    path('crear/', views.crear_reporte, name='crear_reporte'),
    path('<int:reporte_id>/', views.detalle_reporte, name='detalle_reporte'),
    path('<int:reporte_id>/editar/', views.editar_reporte, name='editar_reporte'),
    path('<int:reporte_id>/eliminar/', views.eliminar_reporte, name='eliminar_reporte'),
]
