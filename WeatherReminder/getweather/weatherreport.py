import os
import datetime
import django

django.setup()

from subscription.models import Subscription
from utils import get_geo_coordinates, get_curent_weather


# Open Weather URLs and params for getting geo coordinates and weather data
coordinates_url = 'http://api.openweathermap.org/geo/1.0/direct'
weather_url = 'https://api.openweathermap.org/data/3.0/onecall'
units = 'metric'
exclude = 'minutely,hourly,daily,alerts'
api_key = os.environ.get("OPEN_WEATHER_MAP_API_KEY")
subscriptions = Subscription.objects.all()

for subscription in subscriptions:
    # Getting geo coordinates
    city_name = subscription.city.name
    country_code = subscription.city.country_code
    city_plus_country_code = city_name+','+country_code
    #city_name = 'Uman,UA'
    lat, lon = get_geo_coordinates(city_plus_country_code, api_key, coordinates_url)
    print(lat)
    print(lon)
    # Getting weather results
    weather_report = get_curent_weather(lat, lon, api_key, weather_url, units, exclude)
    print(f'This is a weather report for {city_plus_country_code}')
    print(weather_report)
    # Extracting weather data from the response
    # Time
    unix_timestamp = weather_report['current'].get('dt', 'N/A')
    current_time = datetime.datetime.utcfromtimestamp(unix_timestamp)
    # Temperature
    temperature = weather_report['current'].get('temp', 'N/A')
    feels_like = weather_report['current'].get('feels_like', 'N/A')
    # Pressure, humidity, wind speed
    pressure = weather_report['current'].get('pressure', 'N/A')
    humidity = weather_report['current'].get('humidity', 'N/A')
    wind_speed = weather_report['current'].get('wind_speed', 'N/A')
    # Weather description
    weather_main = weather_report['current'].get('weather', 'N/A')[0].get('main', 'N/A')
    weather_description = weather_report['current'].get('weather', 'N/A')[0].get('description', 'N/A')
    weather_icon_id = weather_report['current'].get('weather', 'N/A')[0].get('icon', 'N/A')
    weather_icon_url = f'https://openweathermap.org/img/wn/{weather_icon_id}@2x.png'

