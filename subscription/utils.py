import requests

from django.core.mail import EmailMessage
from django.core import mail


def get_geo_coordinates(city_name, api_key, url):
    """
    Get the geographical coordinates (latitude and longitude) of a city using an external API.
    :param city_name: str
    :param api_key: str
    :param url: str
    :return: tuple: A tuple containing the latitude and longitude coordinates
    """
    params = {
        'q': city_name,
        'appid': api_key,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data and isinstance(data, list) and len(data) > 0:

            lat = data[0].get('lat')
            lon = data[0].get('lon')
            if lat is not None and lon is not None:
                return lat, lon
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError, TypeError) as e:
        print(f"Response Parsing Error: {e}")

    return None, None


def get_current_weather(lat, lon, api_key, url, units, exclude=None):
    """
    Get current weather forecast for given geo coordinates
    :param lat: str (latitude coordinates)
    :param lon: str (longitude coordinates)
    :param api_key: str
    :param url:
    :param exclude: None or str, if default value is changed
    :param units: None or str, if default value is changed
    :return: dict, containing weather forecast data
    """
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': units,
    }
    if exclude is not None:
        params['exclude'] = exclude
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
         print(f"Request error: {e}")

    return None


def send_weather_report_email(email_data):
    email = EmailMessage(
        subject=email_data["subject"],
        body=email_data["body"],
        to=email_data["to"]
    )
    email.content_subtype = 'html'
    connection = mail.get_connection()
    email.send()
