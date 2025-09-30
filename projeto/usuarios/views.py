from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegistroForm 

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('usuarios:perfil')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Credenciais inválidas')
    return render(request, 'usuarios/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def perfil(request):
    if not request.user.is_authenticated:
        return redirect('usuarios:login')
    return render(request, 'usuarios/perfil.html', {'user': request.user})
