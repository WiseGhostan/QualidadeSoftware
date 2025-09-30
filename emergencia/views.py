from django.shortcuts import render

def numeros_emergencia(request):
    numeros = [
        {'servico': 'Polícia Militar', 'numero': '190'},
        {'servico': 'Corpo de Bombeiros', 'numero': '193'},
        {'servico': 'SAMU (Atendimento Médico)', 'numero': '192'},
        {'servico': 'Defesa Civil', 'numero': '199'},
        {'servico': 'Polícia Civil', 'numero': '(61) 3443-1000'},  # exemplo
        {'servico': 'Disque Denúncia', 'numero': '197'},
        {'servico': 'Central de Atendimento da PMDF', 'numero': '(61) 3214-3333'},
    ]
    return render(request, 'emergencia/home.html', {'numeros': numeros})

