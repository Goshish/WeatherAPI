import csv
import urllib
from datetime import datetime
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
import requests
import json
import datetime



def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        source = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/weather?q=' + city + '&units=metric&lang=ru&appid=c5b5b2772557429ea52552bbcfed9642').read()

        list_of_data = json.loads(source)

        data = {
            'city': city,
            "country_code": str(list_of_data['sys']['country']),
            "coordinate": str(list_of_data['coord']['lon']) + ', ' + str(list_of_data['coord']['lat']),
            "temp": str(list_of_data['main']['temp']) + ' °C',
            "humidity": str(list_of_data['main']['humidity']),
            'main': str(list_of_data['weather'][0]['main']),
            'description': str(list_of_data['weather'][0]['description']),
            'icon': list_of_data['weather'][0]['icon'],
        }
    else:
        data = {}
    return render(request, 'weather_app/index.html', data)


def download_weather_history(request):
    city = request.GET.get('city')  # Получаем название города из GET-параметров

    if not city:
        return HttpResponseBadRequest('Ошибка: Не указан город')

    # Формируем URL для запроса к API OpenWeatherMap
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid=c5b5b2772557429ea52552bbcfed9642'

    # Выполняем запрос к API и получаем данные
    source = urllib.request.urlopen(url).read()
    data = json.loads(source)

    # Создаем CSV файл
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{city}_weather_history.csv"'

    # Записываем данные в CSV файл
    writer = csv.writer(response)
    writer.writerow(['Date', 'Temperature (°C)', 'Humidity', 'Weather Description'])

    # Получаем данные о погоде за последние 5 дней
    for item in data['list'][:5]:
        date = datetime.datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
        temperature = item['main']['temp']
        temperature_celsius = round(temperature - 273.15, 2)
        humidity = item['main']['humidity']
        description = item['weather'][0]['description']
        writer.writerow([date, temperature_celsius, humidity, description])

    return response
