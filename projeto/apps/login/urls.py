from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView   # <-- importe TemplateView aqui
from . import views
from .views import CustomLoginView, alterar_nome, alterar_email

app_name = 'login'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='login/logout.html'), name='logout'),
    path('cadastro/', views.CadastroColaboradorView.as_view(), name='cadastro'),
    path('cadastro/sucesso/', TemplateView.as_view(template_name='login/cadastro_sucesso.html'), name='cadastro_sucesso'),
    path('perfil/', views.perfil, name='perfil'),
    path('alterar-senha/', views.AlterarSenhaView.as_view(), name='alterar_senha'),
    path('senha-alterada/', views.senha_alterada, name='senha_alterada'),
    path('alterar-nome/', alterar_nome, name='alterar_nome'),
    path('alterar-email/', alterar_email, name='alterar_email'),
    path('espaco-do-colaborador/', views.espaco_colaborador, name='espaco_colaborador'),
    path('painel/admin/', TemplateView.as_view(template_name='painel/admin.html'), name='painel_admin'),
    path('painel/colaborador/', TemplateView.as_view(template_name='painel/colaborador.html'), name='painel_colaborador'),
    path('redirecionar/', views.redirecionar_usuario, name='redirecionar_usuario'),
]



