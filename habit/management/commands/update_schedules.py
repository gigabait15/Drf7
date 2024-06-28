from django.core.management import BaseCommand
from habit.tasks import update_schedules


class Command(BaseCommand):
    help = 'Update Celery Beat schedules'

    def handle(self, *args, **kwargs):
        try:
            update_schedules.delay()
            self.stdout.write(self.style.SUCCESS('Schedules successfully updated.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating schedules: {e}'))
