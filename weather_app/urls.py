from django.urls import path

from . import views
from .views import index


urlpatterns = [
    path('', views.index, name='index'),
    path('download-weather-history/', views.download_weather_history, name='download_weather_history'),
]