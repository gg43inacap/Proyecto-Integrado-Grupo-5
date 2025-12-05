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
from django.contrib.auth import views as auth_views

from roles import views as roles_views
from django.views.generic import TemplateView
from . import views as neonatal_views

urlpatterns = [
    path('', neonatal_views.inicio, name='inicio'),
    path('admin/', admin.site.urls),
    path('dashboard/', roles_views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('login/', include('login.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('gestion_some/', include('gestion_some.urls')),
    path('roles/', include('roles.urls')),
]