from django.urls import path
from . import views

app_name = 'eventos'

urlpatterns = [
    path('', views.lista_eventos, name='lista'),
    path('calendario/', views.calendario, name='calendario'),
    path('form/', views.novo_evento, name='form'),
    path('<int:pk>', views.detalhe_evento, name='detalhe'),
    path('<int:pk>/editar/', views.editar_evento, name='editar'),
    path('<int:pk>/inscricao/', views.inscricao_evento, name='inscricao'),
    path('<int:pk>/excluir/', views.excluir_evento, name='excluir'),
]