from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .forms import CadastroColaboradorForm
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

class CadastroColaboradorView(CreateView):
    template_name = 'login/cadastro_colaborador.html'
    form_class = CadastroColaboradorForm
    success_url = reverse_lazy('login:cadastro_sucesso')

    def form_valid(self, form):
        return super().form_valid(form)

@login_required
def perfil(request):
    return render(request, 'login/perfil.html', {'usuario': request.user})

class AlterarSenhaView(PasswordChangeView):
    template_name = 'login/alterar_senha.html'
    success_url = reverse_lazy('login:senha_alterada')


@login_required
def senha_alterada(request):
    return render(request, 'login/senha_alterada.html')

@login_required
def redirecionar_usuario(request):
    user = request.user
    if user.is_superuser:
        return redirect('login:painel_admin')
    elif user.is_staff:
        return redirect('login:espaco_colaborador')
    else:
        return redirect('home')
    
@login_required
def espaco_colaborador(request):
    return render(request, 'painel/colaborador.html')

class CustomLoginView(LoginView):
    template_name = 'login/login.html' 
    redirect_authenticated_user = True
    

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse_lazy('login:painel_admin')
        elif user.is_staff:
            return reverse_lazy('login:espaco_colaborador')
        else:
            return reverse_lazy('login:espaco_colaborador')

@login_required
def alterar_nome(request):
    if request.method == 'POST':
        novo_nome = request.POST.get('novo_nome', '').strip()
        if novo_nome:
            request.user.username = novo_nome
            request.user.save()
            messages.success(request, 'Nome alterado com sucesso!')
            return redirect('login:perfil')
        else:
            messages.error(request, 'Por favor, informe um nome válido.')
    return render(request, 'login/alterar_nome.html')

@login_required
def alterar_email(request):
    if request.method == 'POST':
        novo_email = request.POST.get('novo_email', '').strip()
        if novo_email:
            request.user.email = novo_email
            request.user.save()
            messages.success(request, 'Email alterado com sucesso!')
            return redirect('login:perfil')
        else:
            messages.error(request, 'Por favor, informe um email válido.')
    return render(request, 'login/alterar_email.html')




