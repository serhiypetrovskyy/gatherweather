from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from subscription.views import SubscriptionList, SubscriptionDetail


app_name = 'subscription'

urlpatterns = [
    path('subscriptions/', SubscriptionList.as_view()),
    path('subscriptions/<int:pk>/', SubscriptionDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

