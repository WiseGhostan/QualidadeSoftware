from django.urls import path
from . import views

app_name = 'turistas'

urlpatterns = [
    path('', views.lista_turistas, name='lista'),
    path('cadastro/', views.novo_turista, name='cadastro'),
    path('<int:pk>/', views.detalhe_turista, name='detalhe'),
    path('<int:pk>/editar/', views.editar_turista, name='editar'),
    path('<int:pk>/excluir/', views.excluir_turista, name='excluir'),
]