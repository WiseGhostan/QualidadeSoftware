from django.test import TestCase
from django.urls import reverse

class MapaViewTest(TestCase):
    def test_mapa_view_status_code(self):
        url = reverse('mapa:mapa')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_mapa_view_template_used(self):
        url = reverse('mapa:mapa')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'mapa/mapa.html')

