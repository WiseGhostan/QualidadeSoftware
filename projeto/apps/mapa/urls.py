from django.urls import path
from .views import MapaTuristicoView

app_name = 'mapa'

urlpatterns = [
    path('', MapaTuristicoView.as_view(), name='mapa'),
]
