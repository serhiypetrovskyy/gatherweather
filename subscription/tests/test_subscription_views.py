from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from subscription.models import Subscription, City
from subscription.serializers import SubscriptionSerializer


class SubscriptionListViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='userpassword', email='useremail@gmail.com')
        self.city = City.objects.create(name='Lviv', country_code='UA')
        self.subscription = Subscription.objects.create(city_id=self.city, frequency=1, owner=self.user)
        self.url = reverse('subscription:subscriptions')
        self.client = APIClient()

    def test_subscription_view_GET(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        serializer_data = SubscriptionSerializer([self.subscription, ], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_subscription_view_GET_not_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_subscription_view_POST(self):
        self.client.force_authenticate(user=self.user)
        city_name = 'Uman'
        country_code = 'UA'
        frequency = 1
        response = self.client.post(self.url, {'city_name': city_name, 'country_code': country_code,
                                               'frequency': frequency})
        new_subscription = Subscription.objects.get(pk=2)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(frequency, new_subscription.frequency)

    def test_subscription_view_POST_not_authenticated(self):
        city_name = 'Uman',
        country_code = 'UA',
        frequency = 1
        response = self.client.post(self.url, {'city_name': city_name, 'country_code': country_code,
                                               'frequency': frequency})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class SubscriptionDetailTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='userpassword', email='useremail@gmail.com')
        self.city = City.objects.create(name='Lviv', country_code='UA')
        self.subscription = Subscription.objects.create(city_id=self.city, frequency=1, owner=self.user)
        self.subscription_detail_url = reverse('subscription:subscription_detail', args=[self.subscription.id])
        self.client = APIClient()

    def test_subscription_detail_view_GET(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.subscription_detail_url)
        serializer_data = SubscriptionSerializer([self.subscription, ], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data[0], response.data)

    def test_subscription_view_GET_not_authenticated(self):
        response = self.client.get(self.subscription_detail_url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_subscription_detail_view_PUT(self):
        self.client.force_authenticate(user=self.user)
        city_name = 'Uman'
        country_code = 'UA'
        expected_frequency = 2
        response = self.client.put(self.subscription_detail_url,
                                   {'city_name': city_name, 'country_code': country_code,
                                    'frequency': expected_frequency})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_frequency, response.data['frequency'])
        self.assertEqual(city_name, response.data['city_name'])

    def test_subscription_view_PUT_not_authenticated(self):
        expected_frequency = 2
        response = self.client.put(self.subscription_detail_url,
                                   {'city': self.city.id, 'frequency': expected_frequency})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_subscription_detail_view_DELETE(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.subscription_detail_url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
