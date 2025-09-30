from django.contrib.auth.models import AbstractUser
from django.db import models

class Colaborador(AbstractUser):
    SERVIDOR = 'servidor'
    COLABORADOR = 'colaborador'
    TIPO_CHOICES = [
        (SERVIDOR, 'Servidor da Secretaria de Turismo do GDF'),
        (COLABORADOR, 'Colaborador (Dono de evento)'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

