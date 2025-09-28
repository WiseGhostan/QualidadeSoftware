from django.test import TestCase
from django.urls import reverse

class NumerosEmergenciaViewTest(TestCase):
    def test_view_status_code(self):
        url = reverse('emergencia:emergencia')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_template_usado(self):
        url = reverse('emergencia:emergencia')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'emergencia/home.html')

    def test_contexto_contem_numeros(self):
        url = reverse('emergencia:emergencia')
        response = self.client.get(url)
        self.assertIn('numeros', response.context)

        self.assertIn({'servico': 'Polícia Militar', 'numero': '190'}, response.context['numeros'])
        self.assertIn({'servico': 'SAMU (Atendimento Médico)', 'numero': '192'}, response.context['numeros'])
