from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from subscription.models import Subscription, City
from subscription.serializers import SubscriptionSerializer


class SubscriptionListViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='userpassword', email='useremail@gmail.com')
        self.city = City.objects.create(city_name='Lviv', country_code='UA')
        self.subscription = Subscription.objects.create(city_id=self.city, frequency=1, owner=self.user)
        self.url = reverse('subscription:subscriptions')
        self.client = APIClient()
        self.schedule, self.created = IntervalSchedule.objects.get_or_create(
                every=5,
                period=IntervalSchedule.MINUTES
            )

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
        data = {
            "city_id":
                {
                    "city_name": "Cherkasy",
                    "country_code": "UA"
                },
            "frequency": 1
        }
        response = self.client.post(self.url, data=data, format='json')
        new_subscription = Subscription.objects.get(pk=2)
        task = PeriodicTask.objects.create(
            interval=self.schedule,
            name=self.subscription.id,
            task='subscription.tasks.create_and_send_weather_report_task',
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(data["frequency"], new_subscription.frequency)

    def test_subscription_view_POST_not_authenticated(self):
        data = {
            "city_id":
                {
                    "city_name": "Cherkasy",
                    "country_code": "UA"
                },
            "frequency": 1
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class SubscriptionDetailTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='userpassword', email='useremail@gmail.com')
        self.city = City.objects.create(city_name='Lviv', country_code='UA')
        self.subscription_1 = Subscription.objects.create(city_id=self.city, frequency=1, owner=self.user)
        self.subscription_detail_url = reverse('subscription:subscription_detail', args=[self.subscription_1.id])
        self.client = APIClient()
        self.schedule, self.created = IntervalSchedule.objects.get_or_create(
            every=5,
            period=IntervalSchedule.MINUTES
        )
        self.task = PeriodicTask.objects.create(
            interval=self.schedule,
            name=self.subscription_1.id,
            task='subscription.tasks.create_and_send_weather_report_task',
        )

    def test_subscription_detail_view_GET(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.subscription_detail_url)
        serializer_data = SubscriptionSerializer([self.subscription_1, ], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data[0], response.data)

    def test_subscription_view_GET_not_authenticated(self):
        response = self.client.get(self.subscription_detail_url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_subscription_detail_view_PUT(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "city_id":
                {
                    "city_name": "Cherkasy",
                    "country_code": "UA"
                },
            "frequency": 1
        }
        city_name = data["city_id"]["city_name"]
        response = self.client.put(self.subscription_detail_url, data=data, format='json')
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.MINUTES
        )
        task = PeriodicTask.objects.get(name=self.subscription_1.id)
        task.interval = schedule
        task.save()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data['frequency'], response.data['frequency'])
        self.assertEqual(city_name, response.data['city_id']['city_name'])
        self.assertEqual(task.interval, schedule)

    def test_subscription_view_PUT_not_authenticated(self):
        data = {
            "city_id":
                {
                    "city_name": "Cherkasy",
                    "country_code": "UA"
                },
            "frequency": 1
        }
        city_name = data["city_id"]["city_name"]
        response = self.client.put(self.subscription_detail_url, data=data, format='json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_subscription_detail_view_DELETE(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.subscription_detail_url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
