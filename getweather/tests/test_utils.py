import os

from django.test import TestCase

from getweather.utils import get_geo_coordinates, get_curent_weather


class GeoCoordinatesTestCase(TestCase):
    def setUp(self):
        self.coordinates_url = 'http://api.openweathermap.org/geo/1.0/direct'
        self.api_key = os.environ.get("OPEN_WEATHER_MAP_API_KEY")
        self.city_name = 'Lviv'
        self.country_code = 'UA'
        self.city_plus_country_code = self.city_name + ',' + self.country_code
        self.lviv_lat = 49.841952
        self.lviv_lon = 24.0315921

    def test_get_geo_coordinates(self):
        geo_coordinates = get_geo_coordinates(self.city_plus_country_code, self.api_key, self.coordinates_url)
        self.assertIsInstance(geo_coordinates, tuple)
        self.assertEqual(self.lviv_lat, geo_coordinates[0])
        self.assertEqual(self.lviv_lon, geo_coordinates[1])


class CurrentWeatherTestCase(TestCase):
    def setUp(self):
        self.weather_data_url = 'https://api.openweathermap.org/data/3.0/onecall'
        self.units = 'metric'
        self.exclude = 'minutely,hourly,daily,alerts'
        self.api_key = os.environ.get("OPEN_WEATHER_MAP_API_KEY")
        self.lat = 49.84
        self.lon = 24.03

    def test_get_current_weather(self):
        report = get_curent_weather(self.lat, self.lon, self.api_key, self.weather_data_url, self.units, self.exclude)
        self.assertIsInstance(report, dict)
        self.assertEqual(self.lat, report['lat'])
        self.assertEqual(self.lon, report['lon'])
