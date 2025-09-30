from django.test import TestCase, Client
from django.urls import reverse
from datetime import date
from usuarios.models import Usuario
from .models import Turista

class TuristaViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = Usuario.objects.create_user(username='turista1', password='senha123')
        self.turista = Turista.objects.create(
            usuario=self.usuario,
            nome_completo='João da Silva',
            email='joao@email.com',
            telefone='61999990000',
            data_nascimento=date(1990, 5, 20),
            cidade_origem='São Paulo',
            data_visita=date.today(),
            interesses='Museus, gastronomia'
        )

    def test_lista_turistas(self):
        response = self.client.get(reverse('turistas:lista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.turista.nome_completo)

    def test_detalhe_turista(self):
        response = self.client.get(reverse('turistas:detalhe', args=[self.turista.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.turista.email)

    def test_editar_turista(self):
        self.client.force_login(self.usuario)
        response = self.client.post(reverse('turistas:editar', args=[self.turista.pk]), {
            'nome_completo': 'João Atualizado',
            'email': self.turista.email,
            'telefone': self.turista.telefone,
            'data_nascimento': self.turista.data_nascimento,
            'cidade_origem': self.turista.cidade_origem,
            'data_visita': self.turista.data_visita,
            'interesses': self.turista.interesses
        })
        self.assertEqual(response.status_code, 302)
        self.turista.refresh_from_db()
        self.assertEqual(self.turista.nome_completo, 'João Atualizado')

    def test_excluir_turista(self):
        self.client.force_login(self.usuario)
        response = self.client.post(reverse('turistas:excluir', args=[self.turista.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Turista.objects.filter(pk=self.turista.pk).exists())

