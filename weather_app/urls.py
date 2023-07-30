from django.urls import path

from . import views
from .views import index


urlpatterns = [
    path('', views.index, name='index'),
    path('download-weather/', views.download_weather, name='download_weather'),
]