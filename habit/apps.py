# -*- coding: utf-8 -*-
import os
from django.apps import AppConfig
from django.core.management import call_command


class HabitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'habit'

    def ready(self):
        print(" ready method called.")
        state_file = 'initial_setup_done'

        if not os.path.exists(state_file):
            try:
                if not os.getenv('RUN_MAIN') == 'true':
                    call_command('start_redis')
                    call_command('start_celery_worker')
                    call_command('start_celery_beat')
                    call_command('update_schedules')
                    print("Все команды выполнены успешно.")

                    with open(state_file, 'w') as f:
                        f.write('done')
                    print("Файл initial_setup_done создан.")
            except Exception as e:
                print(f"Error in ready method: {e}")
