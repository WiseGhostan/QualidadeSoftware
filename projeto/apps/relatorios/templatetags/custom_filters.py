# apps/relatorios/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def zip_lists(list1, list2):
    """Filtro para zipar duas listas no template"""
    return zip(list1, list2)

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def divide(value, arg):
    try:
        return value / arg
    except ZeroDivisionError:
        return 0

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def index(l, i):
    try:
        return l[i]
    except IndexError:
        return None
    
@register.filter(name='calcular_variacao')
def calcular_variacao(valor_atual, lista_valores):
    """
    Calcula a variação percentual entre o valor atual e o valor anterior na lista
    """
    try:
        indice_anterior = lista_valores.index(valor_atual) - 1
        if indice_anterior < 0:
            return 0.0
        
        valor_anterior = lista_valores[indice_anterior]
        if valor_anterior == 0:
            return 0.0
            
        variacao = ((valor_atual - valor_anterior) / valor_anterior) * 100
        return round(variacao, 2)
    except (IndexError, TypeError):
        return 0.0