from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('usuarios/', include('usuarios.urls')),
    path('parques/', include('parques.urls', namespace='parques')),
    path('turistas/', include('turistas.urls')),
    path('eventos/', include('eventos.urls')),
    path('relatorios/', include('relatorios.urls')),
    path('mapa/', include('mapa.urls')),
    path('emergencia/', include('emergencia.urls')),
    path('logs/', include('logs.urls')),
    path('accounts/', include('login.urls')),
    path('feiras/', include('feiras.urls')),
    
]
