import json
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from subscription.models import Subscription
from subscription.serializers import SubscriptionSerializer
from subscription.permissions import IsOwner


class SubscriptionList(APIView):
    """
    List all subscriptions or create a new subscription
    """
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get(self, request, format=None):
        subscriptions = Subscription.objects.filter(owner=request.user).all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            subscription = serializer.save(owner=self.request.user)
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=subscription.frequency,
                period=IntervalSchedule.HOURS
            )
            task = PeriodicTask.objects.create(
                interval=schedule,
                name=subscription.id,
                task='subscription.tasks.create_and_send_weather_report_task',
                args=json.dumps([subscription.id]),
            )
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
            updated_subscription = serializer.save()
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=updated_subscription.frequency,
                period=IntervalSchedule.HOURS
            )
            task = PeriodicTask.objects.get(name=subscription.id)
            task.interval = schedule
            task.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        subscription = self.get_object(pk)
        task = PeriodicTask.objects.get(name=pk)
        task.delete()
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

