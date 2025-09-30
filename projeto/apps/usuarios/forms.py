from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telefone = forms.CharField(max_length=15, required=False)
    cpf = forms.CharField(max_length=14, required=True)
    data_nascimento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Usuario
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email',
            'cpf',
            'data_nascimento',
            'telefone',
            'password1', 
            'password2'
        ]

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefone']