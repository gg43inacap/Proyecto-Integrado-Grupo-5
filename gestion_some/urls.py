from django.urls import path # Sistema de rutas de Django
from . import views # Importa las vistas de la aplicación gestion_some
from roles import views as roles_views # Importa vistas de roles para las APIs

urlpatterns = [
    path('madres/verificar_rut/', views.verificar_rut, name='verificar_rut'), # Paso previo: verificar RUT
    path('madres/', views.lista_madres, name='lista_madres'), # Ruta para listar madres
    path('madres/crear/', views.crear_madre, name='crear_madre'), # Ruta para crear madre
    path('madres/<int:madre_id>/', views.detalle_madre, name='detalle_madre'), # Ruta para ver detalles de madre
    path('madres/<int:madre_id>/editar/', views.editar_madre, name='editar_madre'), # Ruta para editar madre
    path('madres/<int:madre_id>/eliminar/', views.eliminar_madre, name='eliminar_madre'), # Ruta para eliminar madre
    path('api/estadisticas/', roles_views.api_estadisticas_some, name='api_estadisticas_some'), # API para estadísticas SOME
    path('api/madre_por_rut/', views.api_madre_por_rut, name='api_madre_por_rut'), # API para autocompletar madre por RUT
]