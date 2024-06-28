# -*- coding: utf-8 -*-
from celery import shared_task, current_app
from datetime import timedelta
from config.settings import TELEGRAM_API
import logging
import requests


logger = logging.getLogger(__name__)


@shared_task
def send_habit_reminder(habit_id):
    try:
        from habit.models import Habit

        habit = Habit.objects.get(id=habit_id)
        user = habit.user
        tg_id = user.tg_id
        useful_action_str = str(habit.useful_action) if habit.useful_action else "no useful action"
        message = f"Напоминание о вашей привычке: {useful_action_str}, в {habit.place}"
        telegram(tg_id, message)
        logger.info(f"Напоминание отправлено по привычке {useful_action_str} - {user.nickname}")
    except Habit.DoesNotExist:
        logger.error(f"Привычка с идентификатором {habit_id} не существует.")
    except Exception as e:
        logger.error(f"Ошибка отправки напоминания о привычке {habit_id}: {str(e)}")


def telegram(tg_id, message):
    params = {
        'text': message,
        'chat_id': tg_id
    }
    response = requests.get(f"https://api.telegram.org/bot{TELEGRAM_API}/sendMessage", params=params).json()
    try:
        if response.get('ok'):
            logger.info(f"Сообщение успешно отправлено на адрес {tg_id}")
        else:
            logger.error(f"Не удалось отправить сообщение на {tg_id}: {response}")
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения  {tg_id}: {e}")


@shared_task
def update_schedules():
    try:
        from habit.models import Habit

        current_app.conf.beat_schedule = {}

        for habit in Habit.objects.all():
            periodicity_days = habit.periodicity
            interval = timedelta(days=periodicity_days)
            current_app.conf.beat_schedule[f'send_habit_reminder_{habit.id}'] = {
                'task': 'tasks.send_habit_reminder',
                'schedule': interval.total_seconds(),
                'args': (habit.id,),
            }

        current_app.conf.on_after_configure()

        logger.info("Schedules successfully updated.")
    except Exception as e:
        logger.error(f"Error updating schedules: {str(e)}")
