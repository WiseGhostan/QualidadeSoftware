from django import forms
from .models import Parque

class ParqueForm(forms.ModelForm):
    class Meta:
        model = Parque
        fields = ['nome', 'endereco']
