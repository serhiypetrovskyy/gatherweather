from django.urls import path

from rest_framework_simplejwt import views as jwt_views

from users.views import registration_view


app_name = 'users'

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
