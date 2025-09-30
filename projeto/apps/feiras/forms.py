from django import forms
from .models import Feira

class FeiraForm(forms.ModelForm):
    class Meta:
        model = Feira
        fields = ['nome', 'endereco']
