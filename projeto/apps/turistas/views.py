from django.shortcuts import render, redirect, get_object_or_404
from .models import Turista
from .forms import TuristaForm 

def lista_turistas(request):
    turistas = Turista.objects.all()
    return render(request, 'turistas/lista.html', {'turistas': turistas})

def novo_turista(request):
    if request.method == 'POST':
        form = TuristaForm(request.POST)
        if form.is_valid():
            turista = form.save(commit=False)  
            turista.usuario = request.user  
            turista.save()                     
            return redirect('turistas:lista')
    else:
        form = TuristaForm()
    return render(request, 'turistas/form.html', {'form': form})


def detalhe_turista(request, pk):
    turista = get_object_or_404(Turista, pk=pk)
    return render(request, 'turistas/detalhe.html', {'turista': turista})

def editar_turista(request, pk):
    turista = get_object_or_404(Turista, pk=pk)
    if request.method == 'POST':
        form = TuristaForm(request.POST, instance=turista)
        if form.is_valid():
            form.save()
            return redirect('turistas:detalhe', pk=pk)
    else:
        form = TuristaForm(instance=turista)
    return render(request, 'turistas/form.html', {'form': form})

def excluir_turista(request, pk):
    turista = get_object_or_404(Turista, pk=pk)
    if request.method == 'POST':
        turista.delete()
        return redirect('turistas:lista')
    return render(request, 'turistas/confirmar_exclusao.html', {'turista': turista})
