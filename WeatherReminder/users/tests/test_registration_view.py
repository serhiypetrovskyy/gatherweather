from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class RegistrationViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('users:register')
        self.username = 'user1'
        self.email = 'user1@email.com'
        self.password = 'user1password'
        self.password2 = 'user1password'

    def test_registration_view(self):
        response = self.client.post(self.url, data={
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'password2': self.password2,
        })
        new_user = User.objects.get(username=self.username)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.username, new_user.username)
        self.assertEqual(self.email, new_user.email)



