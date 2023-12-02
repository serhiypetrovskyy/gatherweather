from django.db import models


class City(models.Model):
    name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=2, default='')


class Subscription(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    frequency = models.IntegerField()
    owner = models.ForeignKey('auth.User', related_name='subscriptions', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']


