"""
Configuración de URLs para el proyecto neonatal.

La lista `urlpatterns` enruta las URLs a las vistas. 
    Para más información, consulta:
    https://docs.djangoproject.com/es/5.2/topics/http/urls/
Ejemplos:
Vistas basadas en funciones
    1. Agrega un import:  from my_app import views
    2. Agrega una URL a urlpatterns:  path('', views.home, name='home')
Vistas basadas en clases
    1. Agrega un import:  from other_app.views import Home
    2. Agrega una URL a urlpatterns:  path('', Home.as_view(), name='home')
Incluyendo otra configuración de URLs
    1. Importa la función include(): from django.urls import include, path
    2. Agrega una URL a urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from roles import views as roles_views
from . import views as neonatal_views

urlpatterns = [
    path('', neonatal_views.inicio, name='inicio'),
    path('sistema-admin-hospitalario/', admin.site.urls),  # URL oculta para admin Django
    path('dashboard/', roles_views.dashboard, name='dashboard'),
    path('login/', include('login.urls')),
    path('logout/', neonatal_views.logout_view, name='logout'),
    path('no-autorizado/', roles_views.no_autorizado, name='no_autorizado'),
    path('gestion_some/', include('gestion_some.urls')),
    path('roles/', include('roles.urls')),
    path('auditoria/', include('auditoria.urls')),
    path('partos/', include('partos.urls')),
    path('reportes/', include('reportes.urls')),  # URLs de reportes cuando esté completa
]