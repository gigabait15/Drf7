from rest_framework import generics
from rest_framework.permissions import AllowAny
from habit.models import Habit
from habit.paginators import HabitPaginator
from habit.serializers import HabitSerializer
from user.permissions import IsUsers


class HabitCreateAPIView(generics.CreateAPIView):
    """отвечает за создание привычки"""
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitListAPIView(generics.ListAPIView):
    """Отвечает за просмотр привычек"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.all()
        else:
            return self.queryset.filter(sign_publicity=True)


class HabitUpdateAPIView(generics.UpdateAPIView):
    """отвечает за редактирование привычки"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsUsers]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """отвечает за удаление привычки"""
    queryset = Habit.objects.all()
    permission_classes = [IsUsers]
