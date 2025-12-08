from django.urls import path
from . import views  # Importa las vistas de la aplicación roles

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),  # Ruta para el panel principal según el rol
    path('usuarios/', views.listar_usuario, name='lista_usuarios'),  # Ruta para listar usuarios
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),  # Ruta para crear usuario
    path('usuarios/<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),  # Ruta para editar usuario
    path('usuarios/<int:pk>/bloquear/', views.bloquear_usuario, name='bloquear_usuario'),  # Ruta para bloquear usuario
]
