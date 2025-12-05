from . import views
from django.urls import path

urlpatterns = [
    # CRUD Parto
    path('partos/', views.lista_partos, name='lista_partos'),
    path('partos/crear/', views.crear_parto, name='crear_parto'),
    path('partos/<int:parto_id>/', views.detalle_parto, name='detalle_parto'),
    path('partos/<int:parto_id>/editar/', views.editar_parto, name='editar_parto'),
    path('partos/<int:parto_id>/eliminar/', views.eliminar_parto, name='eliminar_parto'),
    # CRUD RN
    path('rns/', views.lista_rns, name='lista_rns'),
    path('rns/crear/', views.crear_rn, name='crear_rn'),
    path('rns/<int:rn_id>/', views.detalle_rn, name='detalle_rn'),
    path('rns/<int:rn_id>/editar/', views.editar_rn, name='editar_rn'),
    path('rns/<int:rn_id>/eliminar/', views.eliminar_rn, name='eliminar_rn'),
]
