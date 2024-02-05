from rest_framework.test import APITestCase

from django.urls import resolve, reverse

from rest_framework_simplejwt import views as jwt_views

from users.views import registration_view


class TestSubscriptionURLs(APITestCase):

    def test_user_registration_url(self):
        url = reverse('users:register')
        self.assertEqual(resolve(url).func, registration_view)

    def test_obtain_token_url(self):
        url = reverse('users:token_obtain_pair')
        self.assertEqual(resolve(url).func.view_class, jwt_views.TokenObtainPairView)

    def test_refresh_token_url(self):
        url = reverse('users:token_refresh')
        self.assertEqual(resolve(url).func.view_class, jwt_views.TokenRefreshView)
