from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from subscription.models import Subscription, City
from subscription.serializers import SubscriptionSerializer
from subscription.permissions import IsOwner


class SubscriptionList(APIView):
    """
    List all subscriptions or create a new subscription
    """
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get(self, request, format=None):
        subscriptions = Subscription.objects.all().filter(owner=request.user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        city_name = request.data.get('city_name')
        country_code = request.data.get('country_code').upper()
        if not city_name or not country_code:
            return Response({'error': 'City name and 2 letter country code are required!'},
                            status=status.HTTP_400_BAD_REQUEST)
        city, created = City.objects.get_or_create(name=city_name, country_code=country_code)
        subscription_data = {
            'city': city.id,
            'frequency': request.data.get('frequency')
        }
        serializer = SubscriptionSerializer(data=subscription_data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionDetail(APIView):
    """
    Retrieve, update or delete subscription instance
    """
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_object(self, pk):
        try:
            obj = Subscription.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Subscription.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        subscription = self.get_object(pk)
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        subscription = self.get_object(pk)
        serializer = SubscriptionSerializer(subscription, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        subscription = self.get_object(pk)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

