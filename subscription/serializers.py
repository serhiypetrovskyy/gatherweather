from django.contrib.auth.models import User

from rest_framework import serializers

from subscription.models import Subscription, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'country_code']


class SubscriptionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    city_name = serializers.ReadOnlyField(source='city_id.name')

    class Meta:
        model = Subscription
        fields = ['id', 'city_id', 'city_name', 'frequency', 'owner']


class UserSerializer(serializers.ModelSerializer):
    subscriptions = serializers.PrimaryKeyRelatedField(many=True, queryset=Subscription.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'subscriptions']
