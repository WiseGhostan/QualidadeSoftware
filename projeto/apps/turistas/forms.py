from django import forms
from .models import Turista
from django.core.exceptions import ValidationError
from datetime import date

class TuristaForm(forms.ModelForm):
    class Meta:
        model = Turista
        fields = ['nome_completo', 'email', 'telefone', 'data_nascimento', 
                 'cidade_origem', 'data_visita', 'interesses']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'data_visita': forms.DateInput(attrs={'type': 'date'}),
            'interesses': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_data_nascimento(self):
        data = self.cleaned_data['data_nascimento']
        if data and (date.today().year - data.year) < 12:
            raise ValidationError("O turista deve ter pelo menos 12 anos")
        return data