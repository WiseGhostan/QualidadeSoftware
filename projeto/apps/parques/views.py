from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .forms import ParqueForm
from .models import Parque

def lista_parques(request):
    parques = Parque.objects.all()
    return render(request, 'parques/lista.html', {'parques': parques})

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def cadastrar_parque(request, parque_id=None):
    if parque_id:
        parque = get_object_or_404(Parque, id=parque_id)
    else:
        parque = None

    if request.method == 'POST':
        form = ParqueForm(request.POST, instance=parque)
        if form.is_valid():
            form.save()
            return redirect('parques:gerenciar_parques')
    else:
        form = ParqueForm(instance=parque)

    return render(request, 'parques/form.html', {'form': form, 'parque': parque})

@login_required
@user_passes_test(is_admin)
def gerenciar_parques(request):
    parques = Parque.objects.all()
    form = ParqueForm()

    if request.method == 'POST':
        form = ParqueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('parques:gerenciar_parques')

    return render(request, 'parques/gerenciar.html', {'parques': parques, 'form': form})

@login_required
@user_passes_test(is_admin)
def editar_parque(request, parque_id):
    parque = get_object_or_404(Parque, id=parque_id)
    if request.method == 'POST':
        form = ParqueForm(request.POST, instance=parque)
        if form.is_valid():
            form.save()
            return redirect('parques:gerenciar_parques')
    else:
        form = ParqueForm(instance=parque)

    return render(request, 'parques/editar.html', {'form': form, 'parque': parque})

@login_required
@user_passes_test(is_admin)
def excluir_parque(request, parque_id):
    parque = get_object_or_404(Parque, id=parque_id)
    parque.delete()
    return redirect('parques:gerenciar_parques')
