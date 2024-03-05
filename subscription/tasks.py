import os
import datetime

from celery import shared_task

from subscription.models import Subscription
from subscription.utils import get_geo_coordinates, get_current_weather, send_weather_report_email


# OpenWeather URLs and params for getting geo coordinates and weather data
COORDINATES_URL = 'http://api.openweathermap.org/geo/1.0/direct'
WEATHER_DATA_URL = 'https://api.openweathermap.org/data/3.0/onecall'
UNITS = 'metric'
EXCLUDE = 'minutely,hourly,daily,alerts'
API_KEY = os.environ.get("OPEN_WEATHER_MAP_API_KEY")


@shared_task()
def create_and_send_weather_report_task(subscription_id):
    """
    Take in subscription_id, get required data for API request from the database, make API request, send report via email
    :param subscription_id: int
    """
    subscription = Subscription.objects.get(pk=subscription_id)
    # Get geo coordinates
    city_name = subscription.city_id.city_name
    country_code = subscription.city_id.country_code
    city_plus_country_code = city_name + ',' + country_code
    lat, lon = get_geo_coordinates(city_plus_country_code, API_KEY, COORDINATES_URL)
    # Get weather data
    weather_report = get_current_weather(lat, lon, API_KEY, WEATHER_DATA_URL, UNITS, EXCLUDE)
    # Extracting weather data from the response
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

    email_body = f"""Hello,<br>
        Here is weather forecast you've never subscribed for:<br>
        GatherWeather sends you updates even if you didn't ask. This makes us special.<br>
        There is no 'Unsubscribe' button below, because we'd be sorry to see you go.<br>
        <br>
        {city_name}<br>
        {weather_main}<br>
        {weather_description}<br>
        Temperature: {temperature}<br>
        Feels like: {feels_like}<br>
        Pressure: {pressure}<br>
        Humidity: {humidity}<br>
        Wind speed: {wind_speed}<br>
        <img src="{weather_icon_url}" alt="Weather icon">
    """
    email_data = {
        "subject": "Your latest weather forecast",
        "body": email_body,
        "to": [subscription.owner.email, ]
    }
    send_weather_report_email(email_data)
