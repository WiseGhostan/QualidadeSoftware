from django.shortcuts import render, redirect, get_object_or_404
from .models import Feira
from .forms import FeiraForm
from django.contrib.auth.decorators import login_required

@login_required
def feiras(request):
    feiras = Feira.objects.all()
    return render(request, 'feiras/feiras.html', {'feiras': feiras})

@login_required
def criar_feira(request):
    if request.method == 'POST':
        form = FeiraForm(request.POST)
        if form.is_valid():
            feira = form.save(commit=False)
            feira.save()
            return redirect('feiras:feiras')
    else:
        form = FeiraForm()
    return render(request, 'feiras/form_feiras.html', {'form': form})

@login_required
def editar_feira(request, feira_id):
    feira = get_object_or_404(Feira, id=feira_id)
    if request.method == 'POST':
        form = FeiraForm(request.POST, instance=feira)
        if form.is_valid():
            form.save()
            return redirect('feiras:feiras')
    else:
        form = FeiraForm(instance=feira)
    return render(request, 'feiras/form_feiras.html', {'form': form})

@login_required
def excluir_feira(request, feira_id):
    feira = get_object_or_404(Feira, id=feira_id)
    if request.method == 'POST':
        feira.delete()
        return redirect('feiras:feiras')
    return render(request, 'feiras/confirmar_exclusao.html', {'feira': feiras})

def lista_feiras(request):
    feiras = Feira.objects.all() 
    return render(request, 'feiras/lista_feiras.html', {'feiras': feiras})

