from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

Usuario = get_user_model()

class LogEntry(models.Model):
    TIPOS_ACAO = [
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('CRIAR', 'Criação'),
        ('EDITAR', 'Edição'),
        ('EXCLUIR', 'Exclusão'),
        ('ERRO', 'Erro'),
    ]

    usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='logs_usuario' 
    )
    acao = models.CharField(max_length=7, choices=TIPOS_ACAO)
    modelo = models.CharField(max_length=50)
    objeto_id = models.PositiveIntegerField(null=True, blank=True)
    mensagem = models.TextField()
    ip = models.GenericIPAddressField()
    data_hora = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Entrada de Log'
        verbose_name_plural = 'Logs'
        ordering = ['-data_hora']
        db_table = 'logs_entry'

    def __str__(self):
        return f"{self.get_acao_display()} em {self.modelo} por {self.usuario} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"
