from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from users.serializers import RegisterSerializer


class RegisterSerializerTestCase(APITestCase):
    def test_register_serializer(self):
        data = {
            'username': 'user1',
            'email': 'user1@email.com',
            'password': 'password',
            'password2': 'password',
        }
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        user = User.objects.get(pk=1)
        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.email, data['email'])


