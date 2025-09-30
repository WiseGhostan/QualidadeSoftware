from django.db import models
from django.contrib.auth.models import User

class Feira(models.Model):
    nome = models.CharField(max_length=200)
    endereco = models.TextField()

    def __str__(self):
        return self.nome

