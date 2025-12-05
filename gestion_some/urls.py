from django.urls import path
from . import views

urlpatterns = [
    path('madres/', views.lista_madres, name='lista_madres'),
    path('madres/crear/', views.crear_madre, name='crear_madre'),
    path('madres/<int:madre_id>/', views.detalle_madre, name='detalle_madre'),
    path('madres/<int:madre_id>/editar/', views.editar_madre, name='editar_madre'),
    path('madres/<int:madre_id>/eliminar/', views.eliminar_madre, name='eliminar_madre'),
]