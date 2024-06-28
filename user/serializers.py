from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    """Серилизатор пользователя"""
    class Meta:
        model = User
        fields = ('id', 'nickname', )


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Серилизатор для регистрации пользователя"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('nickname', 'password',)

    def create(self, validated_data):
        user = User.objects.create_user(
            nickname=validated_data['nickname'],
            password=validated_data['password']
        )
        return user
