from django.core.management import BaseCommand
from habit.models import Habit


class Command(BaseCommand):
    """Наполнение базы данных """

    def handle(self, *args, **kwargs):
        # Пример данных курсов
        courses_data = [
            {
                "name": "Course 1",
                "description": "Description of course 1",
                "is_pay": False
            },
            {
                "name": "Course 2",
                "description": "Description of course 2",
                "is_pay": True
            }
        ]

        # Создание курсов
        courses = {}
        for course_data in courses_data:
            course, created = Habit.objects.get_or_create(name=course_data["name"], defaults={
                "description": course_data["description"],
                "is_pay": course_data["is_pay"]
            })
            courses[course_data["name"]] = course

        self.stdout.write(self.style.SUCCESS("База данных успешно наполнена "))
