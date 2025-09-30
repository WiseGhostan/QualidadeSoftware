from django import forms
from .models import Evento
from django.core.exceptions import ValidationError
from datetime import date

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nome', 'descricao', 'tipo', 'data', 'local', 'capacidade', 'valor_ingresso']
        widgets = {
            'data': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_data(self):
        data = self.cleaned_data['data']
        if data.date() < date.today():
            raise ValidationError("A data do evento não pode ser no passado")
        return data