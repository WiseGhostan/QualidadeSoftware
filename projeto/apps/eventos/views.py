from django.shortcuts import render, redirect, get_object_or_404
from .models import Evento, Inscricao 
from .forms import EventoForm 
from datetime import datetime, timedelta
from calendar import Calendar
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def lista_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos/lista.html', {'eventos': eventos})

def calendario(request):
    tipo_evento = request.GET.get('tipo')
    mes_param = request.GET.get('mes')
    
    eventos = Evento.objects.all()
    if tipo_evento:
        eventos = eventos.filter(tipo=tipo_evento)
    
    try:
        mes_atual = datetime.strptime(mes_param, '%Y-%m').date() if mes_param else now().date()
    except ValueError:
        mes_atual = now().date()
    
    mes_atual = mes_atual.replace(day=1)
    mes_anterior = (mes_atual - timedelta(days=1)).replace(day=1)
    mes_proximo = (mes_atual + timedelta(days=32)).replace(day=1)
    
    cal = Calendar(firstweekday=6) 
    semanas = []
    hoje = now().date()

    for semana in cal.monthdayscalendar(mes_atual.year, mes_atual.month):
        semana_dias = []
        for dia in semana:
            if dia == 0:
                semana_dias.append({'dia': '', 'do_mes': False, 'eventos': []})
            else:
                data_dia = mes_atual.replace(day=dia)
                eventos_dia = [
                    e for e in eventos 
                    if e.data.date() == data_dia
                ]
                semana_dias.append({
                    'dia': dia,
                    'do_mes': True,
                    'hoje': data_dia == hoje,
                    'eventos': eventos_dia
                })
        semanas.append(semana_dias)
    
    return render(request, 'eventos/calendario.html', {
        'semanas': semanas,
        'mes_atual': mes_atual,
        'mes_anterior': mes_anterior,
        'mes_proximo': mes_proximo,
        'tipos_evento': Evento.TIPOS_EVENTO,
        'tipo_selecionado': tipo_evento
    })

def novo_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            try:
                evento = form.save()
                messages.success(request, 'Evento criado com sucesso!')
                return redirect('eventos:detalhe', pk=evento.pk)
            except Exception as e:
                messages.error(request, f'Erro ao salvar: {str(e)}')
        else:
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios corretamente.')
    else:
        form = EventoForm()
    
    return render(request, 'eventos/form.html', {'form': form})

def detalhe_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    return render(request, 'eventos/detalhe.html', {'evento': evento})

def inscricao_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')

        Inscricao.objects.create(
            evento=evento,
            nome=nome,
            email=email,
            telefone=telefone
        )

        messages.success(request, 'Inscrição realizada com sucesso!')
        return redirect('eventos:lista')

    return render(request, 'eventos/inscricao.html', {'evento': evento})


def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento atualizado com sucesso!')
            return redirect('eventos:detalhe', pk=evento.pk)
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = EventoForm(instance=evento)

    return render(request, 'eventos/form.html', {'form': form})

@login_required
def excluir_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    
    if request.method == 'POST':
        evento.delete()
        messages.success(request, 'Evento excluído com sucesso.')
        return redirect('eventos:lista')
    
    return render(request, 'eventos/confirmar_exclusao.html', {'evento': evento})