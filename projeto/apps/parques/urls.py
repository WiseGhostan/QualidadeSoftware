from django.urls import path
from . import views

app_name = 'parques'

urlpatterns = [
    path('', views.lista_parques, name='lista'),
    path('cadastrar/', views.cadastrar_parque, name='cadastrar_parque'),
    path('gerenciar/', views.gerenciar_parques, name='gerenciar_parques'),
    path('editar/<int:parque_id>/', views.editar_parque, name='editar_parque'),
    path('excluir/<int:parque_id>/', views.excluir_parque, name='excluir_parque'),
]
