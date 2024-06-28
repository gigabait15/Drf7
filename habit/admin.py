from django.contrib import admin
from habit.models import Habit, EnjoyableHabit, UsefulHabit

admin.site.register(Habit)
admin.site.register(EnjoyableHabit)
admin.site.register(UsefulHabit)
