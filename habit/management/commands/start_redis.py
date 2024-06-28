# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import subprocess


class Command(BaseCommand):
    help = 'Запуск сервера Redis'

    def handle(self, *args, **kwargs):
        try:
            subprocess.Popen(['redis-server'])
            self.stdout.write(self.style.SUCCESS('Сервер Redis успешно запущен'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка запуска сервера Redis: {e}'))
