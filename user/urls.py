from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from user.apps import UserConfig
from user.views import UserRegistrationView

app_name = UserConfig.name


urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name="registration"),
    path('authorization/', TokenObtainPairView.as_view(), name='authorization'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
