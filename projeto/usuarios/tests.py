from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class UsuarioViewsTest(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            username='testeuser',
            password='senha123',
            email='teste@example.com'
        )

    def test_login_view_post_valido(self):
        response = self.client.post(reverse('usuarios:login'), {
            'username': 'testeuser',
            'password': 'senha123'
        })
        self.assertRedirects(response, reverse('home'))

    def test_logout_view(self):
        self.client.login(username='testeuser', password='senha123')
        response = self.client.get(reverse('usuarios:logout'))
        self.assertRedirects(response, reverse('home'))



