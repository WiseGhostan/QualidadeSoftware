from django.db import models
from django.contrib.auth import get_user_model

class Turista(models.Model):
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='turistas')
    nome_completo = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    data_nascimento = models.DateField()
    cidade_origem = models.CharField(max_length=50, blank=True, null=True)
    data_visita = models.DateField()
    interesses = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Turista'
        verbose_name_plural = 'Turistas'
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.nome_completo} - {self.cidade_origem}"