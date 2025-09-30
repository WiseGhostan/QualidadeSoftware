from django.urls import path
from . import views

app_name = 'emergencia'

urlpatterns = [
    path('', views.numeros_emergencia, name='emergencia'),
]
