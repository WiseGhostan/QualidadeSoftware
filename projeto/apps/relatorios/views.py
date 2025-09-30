from venv import logger
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime, timedelta

@login_required
def painel_relatorios(request):
    context = {
        'relatorios_disponiveis': [
            {'nome': 'Gráficos de Turismo', 'url': 'graficos/', 'icone': 'bar-chart'},
            {'nome': 'Visitantes por Mês', 'url': 'visitantes/', 'icone': 'calendar'},
            {'nome': 'Receita do Turismo', 'url': 'receita/', 'icone': 'currency-dollar'},
        ]
    }
    return render(request, 'relatorios/painel.html', context)

@login_required
def graficos_relatorios(request):
    try:
     
        dados_anos = {
            2022: {
                'categorias': ['Parques', 'Feiras', 'Eventos', 'Museus'],
                'visitantes': [10000, 9000, 8000, 4000],
                'titulo': 'Visitantes por Categoria no DF (2022)'
            },
            2023: {
                'categorias': ['Parques', 'Feiras', 'Eventos', 'Museus'],
                'visitantes': [12000, 8500, 11000, 4500],
                'titulo': 'Visitantes por Categoria no DF (2023)'
            },
            2024: {
                'categorias': ['Parques', 'Feiras', 'Eventos', 'Museus'],
                'visitantes': [13000, 9500, 11500, 5000],
                'titulo': 'Visitantes por Categoria no DF (2024)'
            }
        }

        graficos = []

        for ano, dados in dados_anos.items():
            categorias = dados['categorias']
            visitantes = dados['visitantes']
            titulo_grafico = dados['titulo']

            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(categorias, visitantes, color=['#2ecc71', '#3498db', '#e67e22', '#e74c3c'])
            ax.set_title(titulo_grafico)
            ax.set_ylabel('Número de Visitantes')
            ax.grid(True, linestyle='--', alpha=0.3)

            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2., height,
                        f'{int(height)}',
                        ha='center', va='bottom')

            buffer = BytesIO()
            fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            plt.close(fig)

            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

            dados_tabela = list(zip(categorias, visitantes))

            graficos.append({
                'titulo': titulo_grafico,
                'grafico': image_base64,
                'dados': dados_tabela
            })

        context = {
            'graficos': graficos,
            'titulo': 'Relatório de Gráficos por Ano'
        }
        return render(request, 'relatorios/graficos.html', context)

    except Exception as e:
        print(f"Erro ao gerar gráficos: {str(e)}")
        return render(request, 'relatorios/erro.html', {'mensagem': 'Erro ao gerar relatório'})

@login_required
def relatorio_visitantes(request):
    try:
        plt.switch_backend('Agg')

        anos_dados = {
            '2022': {
                'meses': ['Jan/2022', 'Fev/2022', 'Mar/2022', 'Abr/2022', 'Mai/2022', 'Jun/2022'],
                'visitantes': [950, 1100, 1300, 1700, 1600, 1800],
            },
            '2023': {
                'meses': ['Jan/2023', 'Fev/2023', 'Mar/2023', 'Abr/2023', 'Mai/2023', 'Jun/2023'],
                'visitantes': [1200, 1500, 1800, 2100, 1900, 2200],
            },
            '2024': {
                'meses': ['Jan/2024', 'Fev/2024', 'Mar/2024', 'Abr/2024', 'Mai/2024', 'Jun/2024'],
                'visitantes': [1300, 1650, 1900, 2300, 2100, 2400],
            }
        }

        graficos = []

        for ano, dados_ano in anos_dados.items():
            meses = dados_ano['meses']
            visitantes = dados_ano['visitantes']

            if not meses or not visitantes or len(meses) != len(visitantes):
                raise ValueError(f"Dados inconsistentes para {ano}")

            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(meses, visitantes,
                    marker='o',
                    color='#3498db',
                    linewidth=2.5,
                    markersize=8,
                    markerfacecolor='#2ecc71',
                    markeredgecolor='#2c3e50',
                    markeredgewidth=1.5)

            ax.set_title(f'Visitantes Mensais no DF ({ano})', pad=20, fontsize=14, fontweight='bold')
            ax.set_ylabel('Número de Visitantes', labelpad=10)
            ax.grid(True, linestyle='--', alpha=0.4)

            for i, (mes, valor) in enumerate(zip(meses, visitantes)):
                ax.text(mes, valor + 50,
                        f'{valor}',
                        ha='center', va='bottom', fontsize=9,
                        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=2))

            plt.tight_layout()

            buffer = BytesIO()
            fig.savefig(buffer, format='png', dpi=120, bbox_inches='tight', facecolor=fig.get_facecolor())
            plt.close(fig)

            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

            dados_tabela = []
            for i in range(len(meses)):
                variacao = None
                if i > 0:
                    variacao = ((visitantes[i] - visitantes[i - 1]) / visitantes[i - 1]) * 100

                if visitantes[i] < 1500:
                    classificacao = 'Baixa'
                elif visitantes[i] < 2000:
                    classificacao = 'Média'
                else:
                    classificacao = 'Alta'

                dados_tabela.append({
                    'mes': meses[i],
                    'visitantes': visitantes[i],
                    'variacao': variacao,
                    'classificacao': classificacao
                })

            graficos.append({
                'grafico': image_base64,
                'dados': [(d['mes'], d['visitantes'], d['classificacao']) for d in dados_tabela],
                'titulo': f'Visitantes Mensais {ano}'
            })

        context = {
            'graficos': graficos,
            'titulo': 'Relatório de Visitantes Mensais'
        }

        return render(request, 'relatorios/visitantes.html', context)

    except Exception as e:
        logger.error(f"Erro no relatório de visitantes: {str(e)}")
        return HttpResponse(f"Erro ao gerar relatório: {str(e)}", status=500)


@login_required
def relatorio_receita(request):
    trimestres = ['1º Tri', '2º Tri', '3º Tri', '4º Tri']

    receitas_2022 = [4000000, 4300000, 4700000, 5000000]
    receitas_2023 = [4500000, 5200000, 4800000, 5500000]
    receitas_2024 = [4800000, 5400000, 5300000, 5800000]

    def calcular_variacoes(receitas):
        variacoes = []
        for i, val in enumerate(receitas):
            if i == 0:
                variacoes.append(None)  
            else:
                anterior = receitas[i-1]
                variacao = ((val - anterior) / anterior) * 100
                variacoes.append(variacao)
        return variacoes

    variacoes_2022 = calcular_variacoes(receitas_2022)
    variacoes_2023 = calcular_variacoes(receitas_2023)
    variacoes_2024 = calcular_variacoes(receitas_2024)

    def gerar_grafico(ano, receitas, cor):
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.fill_between(trimestres, receitas, color=cor, alpha=0.2)
        ax.plot(trimestres, receitas, marker='o', color=cor)
        ax.set_title(f'Receita do Turismo por Trimestre - {ano}')
        ax.set_ylabel('Receita (R$)')
        ax.grid(True, linestyle='--', alpha=0.3)
        for x, y in zip(trimestres, receitas):
            ax.text(x, y, f'R$ {y/1e6:.1f} mi', ha='center', va='bottom', color=cor)
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        plt.close(fig)
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

    grafico_2022 = gerar_grafico(2022, receitas_2022, 'blue')
    grafico_2023 = gerar_grafico(2023, receitas_2023, 'green')
    grafico_2024 = gerar_grafico(2024, receitas_2024, 'orange')

    graficos = [
        {
            'titulo': '2022',
            'grafico': grafico_2022,
            'dados': [
                {'trimestre': t, 'receita': r, 'variacao': v}
                for t, r, v in zip(trimestres, receitas_2022, variacoes_2022)
            ],
        },
        {
            'titulo': '2023',
            'grafico': grafico_2023,
            'dados': [
                {'trimestre': t, 'receita': r, 'variacao': v}
                for t, r, v in zip(trimestres, receitas_2023, variacoes_2023)
            ],
        },
        {
            'titulo': '2024',
            'grafico': grafico_2024,
            'dados': [
                {'trimestre': t, 'receita': r, 'variacao': v}
                for t, r, v in zip(trimestres, receitas_2024, variacoes_2024)
            ],
        },
    ]

    context = {
        'titulo': 'Relatório de Receita',
        'graficos': graficos,
    }
    return render(request, 'relatorios/receita.html', context)
    