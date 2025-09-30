from django.shortcuts import render
from .models import LogEntry  
from django.http import HttpResponse
import csv

def lista_logs(request):
    logs = LogEntry.objects.all().order_by('-data_hora')
    return render(request, 'logs/lista.html', {'logs': logs})

def busca_logs(request):
    query = request.GET.get('q', '')
    if query:
        logs = LogEntry.objects.filter(acao__icontains=query).order_by('-data_hora')
    else:
        logs = LogEntry.objects.all().order_by('-data_hora')
    return render(request, 'logs/busca.html', {'logs': logs, 'query': query})

def exportar_logs(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="logs.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Data/Hora', 'Usuário', 'Ação', 'IP'])
    
    for log in LogEntry.objects.all():
        writer.writerow([log.data_hora, log.usuario, log.acao, log.ip])
    
    return response
