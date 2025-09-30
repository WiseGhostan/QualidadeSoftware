from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import LogEntry
from django.utils import timezone

User = get_user_model()

class LogEntryModelTest(TestCase):
    def test_str_representation(self):
        user = User.objects.create_user(username='usuario', password='senha123')
        log = LogEntry.objects.create(
            usuario=user,
            acao='LOGIN',
            modelo='TestModel',
            objeto_id=1,
            mensagem='Usuário fez login',
            ip='127.0.0.1',
            data_hora=timezone.now()
        )
        expected_str = f"{log.get_acao_display()} em {log.modelo} por {log.usuario} em {log.data_hora.strftime('%d/%m/%Y %H:%M')}"
        self.assertEqual(str(log), expected_str)
