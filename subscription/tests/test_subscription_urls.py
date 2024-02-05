from rest_framework.test import APITestCase

from django.urls import resolve, reverse

from subscription.views import SubscriptionList, SubscriptionDetail


class TestSubscriptionURLs(APITestCase):

    def test_subscription_url(self):
        url = reverse('subscription:subscriptions')
        self.assertEqual(resolve(url).func.view_class, SubscriptionList)

    def test_subscription_detail_url(self):
        url = reverse('subscription:subscription_detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, SubscriptionDetail)
