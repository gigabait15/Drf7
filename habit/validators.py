from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import time


def validate_max_time(value):
    """Валидатор для проверки времени выполнения привычки"""
    max_time = time(0, 2)
    if value > max_time:
        raise ValidationError(
            _('Время не может быть больше %(max_time)s.'),
            params={'max_time': max_time},
        )


def validate_max_date(value):
    """Валидатор для проверки переодичности выполнения привычки"""
    if int(value) > 7:
        raise ValidationError('Значение периодичности не может быть больше 7 дней.')
