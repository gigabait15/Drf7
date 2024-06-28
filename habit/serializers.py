from rest_framework import serializers
from .models import Habit, UsefulHabit


class UsefulHabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsefulHabit
        fields = '__all__'


class HabitSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField()
    user = serializers.CharField(source='user.nickname')
    periodicity = serializers.CharField(source='get_periodicity_display', read_only=True)
    useful_action = serializers.CharField(write_only=True)
    useful_action_value = serializers.SerializerMethodField()

    class Meta:
        model = Habit
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if isinstance(representation['time'], str):
            representation['time'] = serializers.DateTimeField().to_internal_value(representation['time'])

        # Форматирование времени
        formatted_time = representation['time'].strftime("%Y-%m-%d %H:%M:%S")
        representation['time'] = formatted_time
        return representation

    @staticmethod
    def get_useful_action_value(obj):
        return obj.useful_action.action if obj.useful_action else None

    def create(self, validated_data):
        useful_action_name = validated_data.pop('useful_action', None)
        user = validated_data.pop('user')

        # Найти или создать полезное действие
        if useful_action_name:
            useful_action, created = UsefulHabit.objects.get_or_create(action=useful_action_name)
        else:
            useful_action = None

        # Создать привычку, указав пользователя и полезное действие
        habit = Habit.objects.create(user=user, useful_action=useful_action, **validated_data)

        return habit
