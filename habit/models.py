# -*- coding: utf-8 -*-
from django.db import models
from habit.validators import validate_max_time, validate_max_date
from django.core.exceptions import ValidationError
from config.settings import NULLABLE
from user.models import User


class EnjoyableHabit(models.Model):
    """Модель класса приятной привычки"""
    action = models.CharField(max_length=250, verbose_name='Действие приятной привычки')

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = 'Приятная привычка'
        verbose_name_plural = 'Приятные привычки'


class UsefulHabit(models.Model):
    """Модель класса полезной привычки"""
    action = models.CharField(max_length=250, verbose_name='Действие')

    def __str__(self):
        return f'{str(self.action)}'

    class Meta:
        verbose_name = 'Полезная привычка'
        verbose_name_plural = 'Полезнаые привычки'


class Habit(models.Model):
    """Модель класса привычки"""
    PERIODICITY = (
        (1, 'Раз в день'),
        (2, 'Раз в два дня'),
        (3, 'Раз в три дня'),
        (4, 'Раз в четыре дня'),
        (5, 'Раз в пять дней'),
        (6, 'Раз в шесть дней'),
        (7, 'Раз в неделю'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь', related_name='habbits')
    place = models.CharField(max_length=100, verbose_name='Место')
    time = models.DateTimeField(verbose_name='Время когда выполняется привычка')
    time_complete = models.TimeField(validators=[validate_max_time], verbose_name='Время на выполнение')
    useful_action = models.ForeignKey(UsefulHabit, on_delete=models.CASCADE,
                                      verbose_name='полезная привычка', **NULLABLE)
    enjoyable_action = models.ForeignKey(EnjoyableHabit, on_delete=models.CASCADE,
                                         verbose_name='приятная привычка', **NULLABLE)
    periodicity = models.IntegerField(default=1, choices=PERIODICITY,
                                      validators=[validate_max_date], verbose_name='Периодичность')
    sign_publicity = models.BooleanField(default=False, verbose_name='Признак публичности')
    reward = models.CharField(max_length=250, verbose_name='Вознаграждение', **NULLABLE)
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Связанная привычка',
                                      related_name='related_habits', **NULLABLE)
    sign_pleasant_habit = models.BooleanField(default=False, verbose_name='Признак приятной привычки')

    def clean(self):
        # Проверка на одновременный выбор связанной привычки и вознаграждения
        if self.related_habit and self.reward:
            raise ValidationError('Нельзя указать одновременно связанную привычку и вознаграждение.')

        # Проверка на валидность связанной привычки
        if self.related_habit and not self.sign_pleasant_habit:
            raise ValidationError('В связанные привычки могут попадать только привычки с признаком приятной привычки.')

        # Проверка на валидность приятной привычки
        if self.sign_pleasant_habit and (self.reward or self.related_habit):
            raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')

    def __str__(self):
        useful_action_str = str(self.useful_action) if self.useful_action else None
        return f"PK: {self.pk}, User: {self.user}, Place: {self.place}, Useful Action: {useful_action_str}"

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
