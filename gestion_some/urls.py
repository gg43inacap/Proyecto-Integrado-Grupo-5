from django.urls import path # Sistema de rutas de Django
from . import views # Importa las vistas de la aplicación gestion_some

urlpatterns = [
    path('madres/', views.lista_madres, name='lista_madres'), # Ruta para listar madres
    path('madres/crear/', views.crear_madre, name='crear_madre'), # Ruta para crear madre
    path('madres/<int:madre_id>/', views.detalle_madre, name='detalle_madre'), # Ruta para ver detalles de madre
    path('madres/<int:madre_id>/editar/', views.editar_madre, name='editar_madre'), # Ruta para editar madre
    path('madres/<int:madre_id>/eliminar/', views.eliminar_madre, name='eliminar_madre'), # Ruta para eliminar madre
]