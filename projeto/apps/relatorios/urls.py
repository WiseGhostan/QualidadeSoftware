from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    path('painel/', views.painel_relatorios, name='painel'),
    path('painel/graficos/', views.graficos_relatorios, name='graficos'),
    path('painel/visitantes/', views.relatorio_visitantes, name='visitantes'),
    path('painel/receita/', views.relatorio_receita, name='receita'),
]