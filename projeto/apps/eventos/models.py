from django.db import models
from django.core.validators import MinValueValidator
from datetime import date

class Evento(models.Model):
    TIPOS_EVENTO = [
        ('CUL', 'Cultural'),
        ('MUS', 'Musical'),
        ('ESP', 'Esportivo'),
        ('GAST', 'Gastronômico'),
    ]

    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    tipo = models.CharField(max_length=4, choices=TIPOS_EVENTO)
    data = models.DateTimeField()
    local = models.CharField(max_length=200)
    capacidade = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    valor_ingresso = models.DecimalField(max_digits=8, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['data']

    def __str__(self):
        return f"{self.nome} - {self.get_tipo_display()} ({self.data.strftime('%d/%m/%Y')})"

    @property
    def is_passado(self):
        return self.data.date() < date.today()
    
class Inscricao(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscricoes')
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    criado_em = models.DateTimeField(auto_now_add=True)    