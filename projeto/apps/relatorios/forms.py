from django import forms
from .models import Relatorio

class RelatorioForm(forms.ModelForm):
    class Meta:
        model = Relatorio
        fields = ['tipo', 'parametros']
        widgets = {
            'parametros': forms.HiddenInput()
        }

class FiltroTuristasForm(forms.Form):
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
    ativo = forms.BooleanField(
        label='Somente ativos',
        required=False,
        initial=True
    )

class FiltroEventosForm(forms.Form):
    tipo = forms.ChoiceField(
        choices=[],
        required=False,
        label='Tipo de Evento'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from eventos.models import Evento
        self.fields['tipo'].choices = [('', 'Todos')] + list(Evento.TIPOS_EVENTO)