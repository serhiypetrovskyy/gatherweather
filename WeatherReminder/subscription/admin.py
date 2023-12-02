from django.contrib import admin
# Register your models here.
from subscription.models import Subscription, City


admin.site.register(Subscription)
admin.site.register(City)

