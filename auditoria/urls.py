from . import views
from django.urls import path

urlpatterns = [
    path('', views.lista_auditorias, name='lista_auditorias'),
    path('crear/', views.crear_auditoria, name='crear_auditoria'),
    path('<int:auditoria_id>/', views.detalle_auditoria, name='detalle_auditoria'),
    path('<int:auditoria_id>/editar/', views.editar_auditoria, name='editar_auditoria'),
    path('<int:auditoria_id>/eliminar/', views.eliminar_auditoria, name='eliminar_auditoria'),
]
