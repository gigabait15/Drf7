# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import subprocess


class Command(BaseCommand):
    help = 'Запуск Celery beat'

    def handle(self, *args, **kwargs):
        try:
            subprocess.Popen(['celery', '-A', 'config', 'beat', '--loglevel=info', '--logfile=celery_beat.log'])
            self.stdout.write(self.style.SUCCESS('celery beat стартовал успешно'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при запуске celery beat: {e}'))
