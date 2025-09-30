from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Feira

class FeiraModelTest(TestCase):
    def test_str_representation(self):
        feira = Feira(nome="Feira Central", endereco="Rua das Flores")
        self.assertEqual(str(feira), "Feira Central")

class FeiraViewsTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='usuario', password='senha123')
        self.client = Client()
        self.client.login(username='usuario', password='senha123')

        self.feira = Feira.objects.create(nome="Feira Teste", endereco="Endereço Teste")

    def test_feiras_view_requires_login(self):
        self.client.logout()
        url = reverse('feiras:feiras')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) 

    def test_feiras_view_get(self):
        url = reverse('feiras:feiras')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feiras/feiras.html')
        self.assertIn(self.feira, response.context['feiras'])

    def test_lista_feiras_view(self):
        url = reverse('feiras:lista')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feiras/lista_feiras.html')
        self.assertIn(self.feira, response.context['feiras'])

    def test_criar_feira_get(self):
        url = reverse('feiras:criar_feira')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feiras/form_feiras.html')

    def test_criar_feira_post_valido(self):
        url = reverse('feiras:criar_feira')
        data = {
            'nome': 'Nova Feira',
            'endereco': 'Endereço Nova Feira'
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('feiras:feiras'))
        self.assertTrue(Feira.objects.filter(nome='Nova Feira').exists())

    def test_editar_feira_get(self):
        url = reverse('feiras:editar_feira', args=[self.feira.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feiras/form_feiras.html')

    def test_editar_feira_post_valido(self):
        url = reverse('feiras:editar_feira', args=[self.feira.id])
        data = {
            'nome': 'Feira Editada',
            'endereco': 'Endereço Editado'
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('feiras:feiras'))
        self.feira.refresh_from_db()
        self.assertEqual(self.feira.nome, 'Feira Editada')

    def test_excluir_feira_get(self):
        url = reverse('feiras:excluir_feira', args=[self.feira.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feiras/confirmar_exclusao.html')

    def test_excluir_feira_post(self):
        url = reverse('feiras:excluir_feira', args=[self.feira.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('feiras:feiras'))
        self.assertFalse(Feira.objects.filter(id=self.feira.id).exists())

