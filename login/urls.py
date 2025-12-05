# urls.py para la app login
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
   path('login/', TemplateView.as_view(template_name='login/login.html'), name='login'),
	path('test_login/', TemplateView.as_view(template_name='login/test_login.html'), name='test_login'),
]
