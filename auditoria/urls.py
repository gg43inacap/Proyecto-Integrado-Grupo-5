
from . import views
from django.urls import path

urlpatterns = [
    path('', views.lista_auditorias, name='auditoria_index'),  # Página principal = lista
    path('lista/', views.lista_auditorias, name='lista_auditorias'),  # Lista principal
    path('eventos/', views.lista_auditorias, name='auditoria_eventos'),  # Alias para panel ADMIN
    path('dashboard/', views.lista_auditorias, name='auditoria_dashboard'),  # Redirige a lista (dashboard está en roles)
    path('api/estadisticas/', views.api_estadisticas_auditoria, name='api_estadisticas_auditoria'),  # API de estadísticas
    path('<int:auditoria_id>/', views.detalle_auditoria, name='detalle_auditoria'),  # Solo consulta detalle
    # CRUD ELIMINADO: Los auditores SOLO CONSULTAN
    # Los registros se crean automáticamente por el sistema
    # path('crear/', ...) - NO DISPONIBLE
    # path('editar/', ...) - NO DISPONIBLE  
    # path('eliminar/', ...) - NO DISPONIBLE
]
