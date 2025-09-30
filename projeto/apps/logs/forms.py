from django import forms
from .models import LogEntry

class FiltroLogsForm(forms.Form):
    acao = forms.ChoiceField(
        choices=[('', 'Todas')] + LogEntry.TIPOS_ACAO,
        required=False,
        label='Tipo de Ação'
    )
    data_inicio = forms.DateField(
        label='Data Início',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    data_fim = forms.DateField(
        label='Data Fim',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    usuario = forms.CharField(
        label='Usuário',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Nome ou username'})
    )