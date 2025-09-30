from django.urls import path
from . import views

app_name = 'feiras'

urlpatterns = [
    path('feiras/', views.feiras, name='feiras'),
    path('lista/', views.lista_feiras, name='lista'),
    path('criar/', views.criar_feira, name='criar_feira'),
    path('editar/<int:feira_id>/', views.editar_feira, name='editar_feira'),
    path('excluir/<int:feira_id>/', views.excluir_feira, name='excluir_feira'),
]
