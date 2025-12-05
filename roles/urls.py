from django.urls import path
from . import views  # Importa las vistas de la aplicación roles

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),  # Ruta para el panel principal según el rol
    path('users/', views.user_list, name='user_list'),  # Ruta para listar usuarios
    path('users/create/', views.user_create, name='user_create'),  # Ruta para crear usuario
    path('users/<int:pk>/edit/', views.user_update, name='user_update'),  # Ruta para editar usuario
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),  # Ruta para eliminar usuario
]
