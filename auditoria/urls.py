
from . import views
from django.urls import path

urlpatterns = [
    path('', views.lista_auditorias, name='lista_auditorias'),
    # path('crear/', views.crear_auditoria, name='crear_auditoria'), # TEMPORAL: solo para poblar la DB. Descomentar solo si necesitas poblar la tabla manualmente.
    path('<int:auditoria_id>/', views.detalle_auditoria, name='detalle_auditoria'),
    # Las rutas de editar/eliminar están deshabilitadas porque no existen esas vistas
    # path('<int:auditoria_id>/editar/', views.editar_auditoria, name='editar_auditoria'),
    # path('<int:auditoria_id>/eliminar/', views.eliminar_auditoria, name='eliminar_auditoria'),
]
