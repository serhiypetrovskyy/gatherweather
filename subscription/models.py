from django.db import models


class City(models.Model):
    name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=2, default='')

    def __str__(self):
        return self.name


class Subscription(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)
    frequency = models.IntegerField()
    owner = models.ForeignKey('auth.User', related_name='subscriptions', on_delete=models.CASCADE)

    def __str__(self):
        name = f"{self.city_id} by {self.owner}"
        return name

    class Meta:
        ordering = ['created']


