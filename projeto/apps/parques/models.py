from django.db import models

class Parque(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return self.nome
