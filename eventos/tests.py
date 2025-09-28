from django.test import TestCase
from django.urls import reverse
from .models import Evento
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from decimal import Decimal

class EventoModelTest(TestCase):
    def setUp(self):
        self.evento = Evento.objects.create(
            nome="Feira de Sabores",
            descricao="Comidas típicas de várias regiões",
            tipo="GAST",
            data=make_aware(datetime.now() + timedelta(days=10)),
            local="Parque da Cidade",
            capacidade=100,
            valor_ingresso=Decimal('25.00')
        )

    def test_criacao_evento(self):
        self.assertEqual(self.evento.nome, "Feira de Sabores")
        self.assertEqual(self.evento.tipo, "GAST")
        self.assertEqual(self.evento.capacidade, 100)
        self.assertFalse(self.evento.is_passado)

    def test_str_method(self):
        expected_str = f"{self.evento.nome} - {self.evento.get_tipo_display()} ({self.evento.data.strftime('%d/%m/%Y')})"
        self.assertEqual(str(self.evento), expected_str)

    def test_is_passado_true(self):
        evento_antigo = Evento.objects.create(
            nome="Show Antigo",
            descricao="Evento que já passou",
            tipo="MUS",
            data=make_aware(datetime.now() - timedelta(days=5)),
            local="Centro Cultural",
            capacidade=200,
            valor_ingresso=Decimal('50.00')
        )
        self.assertTrue(evento_antigo.is_passado)


class EventoViewsTest(TestCase):
    def setUp(self):
        self.evento = Evento.objects.create(
            nome="Evento Teste",
            descricao="Descrição de teste",
            tipo="CUL",
            data=make_aware(datetime(2025, 6, 20)),
            local="Auditório",
            capacidade=50,
            valor_ingresso=Decimal('30.00')
        )

    def test_lista_eventos_view(self):
        url = reverse('eventos:lista')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eventos/lista.html')
        self.assertIn(self.evento, response.context['eventos'])

    def test_calendario_view(self):
        url = reverse('eventos:calendario')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eventos/calendario.html')

    def test_detalhe_evento_view(self):
        url = reverse('eventos:detalhe', args=[self.evento.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eventos/detalhe.html')
        self.assertEqual(response.context['evento'], self.evento)

    def test_novo_evento_view_get(self):
        url = reverse('eventos:form')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eventos/form.html')

    def test_editar_evento_view_get(self):
        url = reverse('eventos:editar', args=[self.evento.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eventos/form.html')

