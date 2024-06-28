from rest_framework import generics
from user.serializers import UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    """Представление для создание(регистрации) пользователя"""
    serializer_class = UserRegistrationSerializer
