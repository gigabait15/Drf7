# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import subprocess


class Command(BaseCommand):
    help = 'Запуск Celery worker'

    def handle(self, *args, **kwargs):
        try:
            subprocess.Popen(['celery', '-A', 'config', 'worker', '--loglevel=info', '-P', 'eventlet',
                              '--logfile=celery_worker.log'])
            self.stdout.write(self.style.SUCCESS('celery worker стартовал успешно'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при запуске celery worker: {e}'))
