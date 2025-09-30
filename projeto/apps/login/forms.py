from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Colaborador

class CadastroColaboradorForm(UserCreationForm):
    tipo = forms.ChoiceField(
        choices=Colaborador.TIPO_CHOICES,
        widget=forms.RadioSelect,
        label="Tipo de usuário"
    )

    class Meta:
        model = Colaborador
        fields = ['username', 'email', 'tipo', 'password1', 'password2']

