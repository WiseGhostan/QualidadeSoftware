from django.urls import path
from . import views

app_name = 'logs'

urlpatterns = [
    path('', views.lista_logs, name='lista'),
    path('busca/', views.busca_logs, name='busca'),
    path('exportar/', views.exportar_logs, name='exportar'),
]