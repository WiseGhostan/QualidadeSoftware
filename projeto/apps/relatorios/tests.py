from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date
from .models import DadosTurismoAnual, PaisEmissor, RotaAerea, EventoDestaque

class DadosTurismoAnualTest(TestCase):
    def test_criacao_valida(self):
        dados = DadosTurismoAnual.objects.create(
            ano=2024,
            viagens_domesticas=500,
            variacao_viagens=5.0,
            gasto_medio=800.50,
            motivo_lazer=40.0,
            motivo_visita=30.0,
            motivo_saude=20.0,
            motivo_outros=10.0,
            transporte_carro=40.0,
            transporte_aviao=30.0,
            transporte_onibus_excursao=10.0,
            transporte_onibus_linha=10.0,
            transporte_outros=10.0,
            turistas_internacionais=120,
            variacao_internacional=3.2,
            ocupacao_hoteleira=75.5,
            contribuicao_pib=2.4,
            arrecadacao_iss=1200000.00
        )
        self.assertEqual(str(dados), "Dados de Turismo DF - 2024")

    def test_validacao_motivos_incorretos(self):
        dados = DadosTurismoAnual(
            ano=2025,
            viagens_domesticas=400,
            variacao_viagens=2.0,
            gasto_medio=700.00,
            motivo_lazer=30.0,
            motivo_visita=30.0,
            motivo_saude=30.0,
            motivo_outros=20.0, 
            transporte_carro=25.0,
            transporte_aviao=25.0,
            transporte_onibus_excursao=20.0,
            transporte_onibus_linha=15.0,
            transporte_outros=15.0,
            turistas_internacionais=100,
            variacao_internacional=1.0,
            ocupacao_hoteleira=60.0,
            contribuicao_pib=2.0,
            arrecadacao_iss=900000.00
        )
        with self.assertRaises(ValidationError):
            dados.full_clean()

class PaisEmissorTest(TestCase):
    def test_criacao_pais_emissor(self):
        pais = PaisEmissor.objects.create(
            nome="Argentina",
            posicao_ranking=1,
            percentual=25.5
        )
        self.assertEqual(str(pais), "1º - Argentina (25.5%)")

class RotaAereaTest(TestCase):
    def test_criacao_rota(self):
        rota = RotaAerea.objects.create(
            destino="Buenos Aires",
            pais="Argentina",
            ativa=True,
            data_inicio=date(2024, 1, 1),
            voos_semanais=4
        )
        self.assertEqual(str(rota), "Voo para Buenos Aires, Argentina")

class EventoDestaqueTest(TestCase):
    def test_criacao_evento(self):
        evento = EventoDestaque.objects.create(
            nome="Expo Turismo",
            tipo="FEIRA",
            data_inicio=date(2024, 9, 1),
            data_fim=date(2024, 9, 3),
            visitantes_estimados=10000,
            impacto_economico=1500000.00,
            descricao="Feira internacional de turismo"
        )
        self.assertEqual(str(evento), "Expo Turismo (2024)")

