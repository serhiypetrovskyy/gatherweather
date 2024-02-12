from django.contrib.auth.models import User

from rest_framework import serializers

from subscription.models import Subscription, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name', 'country_code']


class SubscriptionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    city_id = CitySerializer()

    class Meta:
        model = Subscription
        fields = ['id', 'city_id', 'frequency', 'owner']

    def create(self, validated_data):
        city_data = validated_data.pop('city_id')
        city_name = city_data['city_name']
        country_code = city_data['country_code']
        city, created = City.objects.get_or_create(city_name=city_name, country_code=country_code)
        subscription = Subscription.objects.create(city_id=city, **validated_data)
        return subscription

    def update(self, instance, validated_data):
        city_data = validated_data.pop('city_id')
        city_name = city_data['city_name']
        country_code = city_data['country_code']
        city, created = City.objects.get_or_create(city_name=city_name, country_code=country_code)
        instance.city_id = city
        instance.frequency = validated_data.get('frequency', instance.frequency)
        return instance

    def validate_city_id(self, value):
        """Varify the string contains letters only"""
        if any(not item.isalpha() for item in value.values()):
            raise serializers.ValidationError("Must contain letters only!")
        if len(value['country_code']) < 2:
            raise serializers.ValidationError("Country code must be a 2-letter value!")
        return value


class UserSerializer(serializers.ModelSerializer):
    subscriptions = serializers.PrimaryKeyRelatedField(many=True, queryset=Subscription.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'subscriptions']
