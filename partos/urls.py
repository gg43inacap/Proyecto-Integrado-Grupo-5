from . import views # Importa las vistas de la aplicación partos
from django.urls import path # Sistema de rutas de Django

urlpatterns = [
    # CRUD Parto
    path('partos/', views.lista_partos, name='lista_partos'), # Ruta para listar partos
    path('partos/crear/', views.crear_parto, name='crear_parto'), # Ruta para crear parto
    path('partos/<int:parto_id>/', views.detalle_parto, name='detalle_parto'), # Ruta para ver detalles de parto
    path('partos/<int:parto_id>/editar/', views.editar_parto, name='editar_parto'), # Ruta para editar parto
    # CRUD RN
    path('rns/', views.lista_rns, name='lista_rns'), # Ruta para listar recién nacidos
    path('rns/crear/', views.crear_rn, name='crear_rn'), # Ruta para crear recién nacido
    path('rns/crear-multiples/', views.crear_rns, name='crear_rns'), # Ruta para crear múltiples recién nacidos
    path('rns/<int:rn_id>/', views.detalle_rn, name='detalle_rn'), # Ruta para ver detalles de recién nacido
    path('rns/<int:rn_id>/editar/', views.editar_rn, name='editar_rn'), # Ruta para editar recién nacido
    # Nuevas funcionalidades
    path('ajax/filtrar-partos/', views.filtrar_partos_por_madre, name='filtrar_partos_por_madre'), # Ruta AJAX para filtrar partos
    path('api/estadisticas_matrona/', views.api_estadisticas_matrona, name='partos_api_estadisticas_matrona'),
    path('partos/<int:parto_id>/completar/', views.completar_parto, name='completar_parto'), # Ruta para completar parto
]
