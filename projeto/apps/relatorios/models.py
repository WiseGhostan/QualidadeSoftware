from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError

class DadosTurismoAnual(models.Model):
    ano = models.PositiveIntegerField(
        unique=True,
        verbose_name="Ano de referência",
        validators=[MinValueValidator(2019), MaxValueValidator(2050)]
    )
    
    # Viagens domésticas
    viagens_domesticas = models.PositiveIntegerField(
        verbose_name="Viagens domésticas (em milhares)",
        help_text="Número total de viagens domésticas para o DF"
    )
    variacao_viagens = models.FloatField(
        verbose_name="Variação percentual de viagens",
        help_text="Variação em relação ao ano anterior (%)"
    )
    
    # Gastos turísticos
    gasto_medio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Gasto médio por viagem (R$)",
        help_text="Gasto médio por viagem com pernoite"
    )

    motivo_lazer = models.FloatField(
        verbose_name="Viagens por lazer (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    motivo_visita = models.FloatField(
        verbose_name="Viagens para visitar familiares/eventos (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    motivo_saude = models.FloatField(
        verbose_name="Viagens para tratamento de saúde (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    motivo_outros = models.FloatField(
        verbose_name="Outros motivos de viagem (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    transporte_carro = models.FloatField(
        verbose_name="Uso de carro particular/empresa (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    transporte_aviao = models.FloatField(
        verbose_name="Uso de avião (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    transporte_onibus_excursao = models.FloatField(
        verbose_name="Uso de ônibus de excursão/fretado (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    transporte_onibus_linha = models.FloatField(
        verbose_name="Uso de ônibus de linha (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    transporte_outros = models.FloatField(
        verbose_name="Outros meios de transporte (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    turistas_internacionais = models.PositiveIntegerField(
        verbose_name="Turistas estrangeiros (em milhares)"
    )
    variacao_internacional = models.FloatField(
        verbose_name="Variação turismo internacional (%)"
    )

    ocupacao_hoteleira = models.FloatField(
        verbose_name="Taxa de ocupação hoteleira (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    contribuicao_pib = models.FloatField(
        verbose_name="Contribuição para o PIB do DF (%)"
    )
    arrecadacao_iss = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Arrecadação de ISS (em milhões R$)"
    )
   
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Dados Anuais de Turismo"
        verbose_name_plural = "Dados Anuais de Turismo"
        ordering = ['-ano']
    
    def __str__(self):
        return f"Dados de Turismo DF - {self.ano}"
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def clean(self):
        total_motivos = sum([
            self.motivo_lazer,
            self.motivo_visita,
            self.motivo_saude,
            self.motivo_outros
        ])
        if round(total_motivos, 1) != 100:
            raise ValidationError("A soma dos percentuais de motivos de viagem deve ser 100%")

        total_transportes = sum([
            self.transporte_carro,
            self.transporte_aviao,
            self.transporte_onibus_excursao,
            self.transporte_onibus_linha,
            self.transporte_outros
        ])
        if round(total_transportes, 1) != 100:
            raise ValidationError("A soma dos percentuais de meios de transporte deve ser 100%")

class PaisEmissor(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    posicao_ranking = models.PositiveIntegerField()
    percentual = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentual do total de turistas internacionais"
    )
    
    class Meta:
        verbose_name = "País Emissor"
        verbose_name_plural = "Países Emissores"
        ordering = ['posicao_ranking']
    
    def __str__(self):
        return f"{self.posicao_ranking}º - {self.nome} ({self.percentual}%)"

class RotaAerea(models.Model):
    destino = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    ativa = models.BooleanField(default=True)
    data_inicio = models.DateField()
    voos_semanais = models.PositiveIntegerField(default=1)
    
    class Meta:
        verbose_name = "Rota Aérea Internacional"
        verbose_name_plural = "Rotas Aéreas Internacionais"
        ordering = ['pais', 'destino']
    
    def __str__(self):
        return f"Voo para {self.destino}, {self.pais}"

class EventoDestaque(models.Model):
    TIPOS_EVENTO = [
        ('FEIRA', 'Feira/Exposição'),
        ('ESPORTE', 'Evento Esportivo'),
        ('SHOW', 'Show/Espetáculo'),
        ('CONGRESSO', 'Congresso/Convenção'),
        ('OUTRO', 'Outro')
    ]
    
    nome = models.CharField(max_length=200)
    tipo = models.CharField(max_length=10, choices=TIPOS_EVENTO)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    visitantes_estimados = models.PositiveIntegerField()
    impacto_economico = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Impacto econômico (R$)"
    )
    descricao = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Evento de Destaque"
        verbose_name_plural = "Eventos de Destaque"
        ordering = ['-data_inicio']
    
    def __str__(self):
        return f"{self.nome} ({self.data_inicio.year})"