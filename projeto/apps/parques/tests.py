from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Parque

User = get_user_model()

class ParquesViewsTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='user', password='userpass')

        self.admin = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')

        self.parque = Parque.objects.create(nome='Parque Teste', endereco='Endereco Teste')

    def test_lista_parques_view(self):
        url = reverse('parques:lista')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parques/lista.html')

    def test_gerenciar_parques_view_requires_login_and_admin(self):
        url = reverse('parques:gerenciar_parques')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

        self.client.login(username='user', password='userpass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
        self.client.logout()

        self.client.login(username='admin', password='adminpass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parques/gerenciar.html')
        self.client.logout()

    def test_cadastrar_parque_get_and_post(self):
        url = reverse('parques:cadastrar_parque')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

        self.client.login(username='user', password='userpass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
        self.client.logout()

        self.client.login(username='admin', password='adminpass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parques/form.html')

        data = {'nome': 'Parque Novo', 'endereco': 'Endereco Novo'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Parque.objects.filter(nome='Parque Novo').exists())
        self.client.logout()

    def test_editar_parque_view(self):
        url = reverse('parques:editar_parque', args=[self.parque.id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

        self.client.login(username='user', password='userpass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
        self.client.logout()

        self.client.login(username='admin', password='adminpass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parques/editar.html')

        data = {'nome': 'Parque Editado', 'endereco': 'Endereco Editado'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.parque.refresh_from_db()
        self.assertEqual(self.parque.nome, 'Parque Editado')
        self.client.logout()

    def test_excluir_parque_view(self):
        url = reverse('parques:excluir_parque', args=[self.parque.id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

        self.client.login(username='user', password='userpass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
        self.client.logout()

        self.client.login(username='admin', password='adminpass')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Parque.objects.filter(id=self.parque.id).exists())
        self.client.logout()



