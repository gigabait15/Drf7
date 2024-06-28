# -*- coding: utf-8 -*-
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, nickname, password=None, **extra_fields):
        """
        Создает и возвращает пользователя с заданным nickname и паролем.
        """
        if not nickname:
            raise ValueError('Поле Nickname должно быть заполнено')
        user = self.model(nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, password=None, **extra_fields):
        """
        Создает и возвращает суперпользователя с заданным nickname и паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(nickname, password, **extra_fields)


class User(AbstractUser):
    username = None
    nickname = models.CharField(max_length=50, unique=True, verbose_name='ник')
    tg_id = models.PositiveIntegerField(default=503234730, verbose_name='id для телеграма')

    USERNAME_FIELD = "nickname"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.nickname
