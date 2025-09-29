from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

User = get_user_model()

class LoginViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='usuario', password='senha123', email='usuario@teste.com')

    def test_cadastro_colaborador_view_get(self):
        url = reverse('login:cadastro')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/cadastro_colaborador.html')

    def test_cadastro_colaborador_view_post(self):
        url = reverse('login:cadastro')
        data = {
            'username': 'novo_usuario',
            'password1': 'SenhaForte123!',
            'password2': 'SenhaForte123!',
            'email': 'novo@teste.com',
            'tipo': User.TIPO_CHOICES[0][0],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='novo_usuario').exists())

    def test_login_view_get(self):
        url = reverse('login:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/login.html')

    def test_login_view_post_success(self):
        url = reverse('login:login')
        data = {
            'username': 'usuario',
            'password': 'senha123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_perfil_view_requires_login(self):
        url = reverse('login:perfil')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username='usuario', password='senha123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/perfil.html')
        self.assertEqual(response.context['usuario'], self.user)

    def test_alterar_nome_get_and_post(self):
        url = reverse('login:alterar_nome')
        self.client.login(username='usuario', password='senha123')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/alterar_nome.html')

        response = self.client.post(url, {'novo_nome': 'novo_usuario_nome'})
        self.assertRedirects(response, reverse('login:perfil'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'novo_usuario_nome')

        response = self.client.post(url, {'novo_nome': ''})
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Por favor, informe um nome válido.' in str(m) for m in messages))

    def test_alterar_email_get_and_post(self):
        url = reverse('login:alterar_email')
        self.client.login(username='usuario', password='senha123')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/alterar_email.html')

        response = self.client.post(url, {'novo_email': 'novoemail@teste.com'})
        self.assertRedirects(response, reverse('login:perfil'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'novoemail@teste.com')

        response = self.client.post(url, {'novo_email': ''})
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Por favor, informe um email válido.' in str(m) for m in messages))

    def test_senha_alterada_view_requires_login(self):
        url = reverse('login:senha_alterada')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) 

        self.client.login(username='usuario', password='senha123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/senha_alterada.html')

    def test_redirecionar_usuario_view(self):
        self.client.login(username='usuario', password='senha123')

        response = self.client.get(reverse('login:redirecionar_usuario'))
        self.assertRedirects(response, reverse('home'))

        self.user.is_superuser = True
        self.user.save()
        response = self.client.get(reverse('login:redirecionar_usuario'))
        self.assertRedirects(response, reverse('login:painel_admin'))

        self.user.is_superuser = False
        self.user.is_staff = True
        self.user.save()
        response = self.client.get(reverse('login:redirecionar_usuario'))
        self.assertRedirects(response, reverse('login:espaco_colaborador'))

    def test_espaco_colaborador_view_requires_login(self):
        url = reverse('login:espaco_colaborador')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username='usuario', password='senha123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'painel/colaborador.html')

