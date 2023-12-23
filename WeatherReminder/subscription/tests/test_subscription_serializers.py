from django.contrib.auth.models import User
from django.test import TestCase

from subscription.models import Subscription, City
from subscription.serializers import SubscriptionSerializer, CitySerializer, UserSerializer


class CitySerializerTestCase(TestCase):
    def test_city_serializer(self):
        city = City.objects.create(name='Lviv', country_code='UA')
        city_1 = City.objects.create(name='Uman', country_code='UA')
        data = CitySerializer([city, city_1], many=True).data
        expected_data = [
            {
                'id': 1,
                'name': 'Lviv',
                'country_code': 'UA',
            },
            {
                'id': 2,
                'name': 'Uman',
                'country_code': 'UA',
            },
        ]
        self.assertEqual(expected_data, data)


class UserSerializerTestCase(TestCase):
    def test_user_serializer(self):
        user = User.objects.create(username='user', password='userpassword', email='useremail@gmail.com')
        user_1 = User.objects.create(username='user1', password='userpassword1', email='user1email@gmail.com')
        data = UserSerializer([user, user_1], many=True).data
        expected_data = [
            {
                'id': 1,
                'username': 'user',
                'subscriptions': [],
            },
            {
                'id': 2,
                'username': 'user1',
                'subscriptions': [],
            },
        ]
        self.assertEqual(expected_data, data)


class SubscriptionSerializerTestCase(TestCase):
    def test_subscription_serializer(self):
        user = User.objects.create(username='user', password='userpassword', email='useremail@gmail.com')
        city = City.objects.create(name='Lviv', country_code='UA')
        subscription = Subscription.objects.create(city=city, frequency=1, owner=user)
        data = SubscriptionSerializer(subscription).data
        expected_data = {
                'id': 1,
                'city': 1,
                'frequency': 1,
                'owner': 'user',
            }
        self.assertEqual(expected_data, data)
