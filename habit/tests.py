from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from django.urls import reverse
from .models import EnjoyableHabit, UsefulHabit, Habit
from user.models import User
from django.utils import timezone
from .serializers import HabitSerializer


class HabitModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(nickname='testuser', password='password')
        self.enjoyable_habit = EnjoyableHabit.objects.create(action='Read a book')
        self.useful_habit = UsefulHabit.objects.create(action='Exercise')

    def test_create_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place='Park',
            time=timezone.now(),
            time_complete='00:01:30',
            useful_action=self.useful_habit,
            enjoyable_action=self.enjoyable_habit,
            periodicity=1,
            sign_publicity=True,
            reward='Ice cream',
            sign_pleasant_habit=False
        )
        self.assertEqual(habit.user.nickname, 'testuser')
        self.assertEqual(habit.place, 'Park')
        self.assertEqual(habit.useful_action.action, 'Exercise')
        self.assertEqual(habit.enjoyable_action.action, 'Read a book')

    def test_clean_method(self):
        habit = Habit(
            user=self.user,
            place='Test Place',
            time=timezone.now(),
            time_complete='00:01:00',
            useful_action=self.useful_habit,
            enjoyable_action=self.enjoyable_habit,
            periodicity=1,
            sign_publicity=True,
            reward='Test Reward',
            related_habit=None,
            sign_pleasant_habit=False,
        )
        habit.full_clean()


class HabitAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(nickname='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        self.useful_habit = UsefulHabit.objects.create(action='Exercise')
        self.enjoyable_habit = EnjoyableHabit.objects.create(action='Read a book')
        self.habit = Habit.objects.create(
            user=self.user,
            place='Park',
            time="2024-06-24 16:24:04",
            time_complete='00:01:00',
            useful_action=self.useful_habit,
            enjoyable_action=self.enjoyable_habit,
            periodicity=1,
            sign_publicity=True,
            reward='Ice cream',
            sign_pleasant_habit=False
        )

    def test_create_habit(self):
        url = reverse('habit:habit_create')
        data = {
            'place': 'Gym',
            'user': 'test',
            'time': "2024-06-24 16:24",
            'time_complete': '00:01',
            'useful_action': self.useful_habit.pk,
            'periodicity': 1,
            'sign_publicity': True,
            'reward': 'Protein Shake',
            'sign_pleasant_habit': False

        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_habits(self):
        url = reverse('habit:habit_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_update_habit(self):
        url = reverse('habit:habit_update', kwargs={'pk': self.habit.pk})
        data = {
            'place': 'Gym',
            'time': "2024-06-24 16:24",
            'time_complete': '00:01',
            'useful_action': self.useful_habit.pk,
            'periodicity': 1,
            'sign_publicity': True,
            'sign_pleasant_habit': False
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_delete_habit(self):
        url = reverse('habit:habit_delete', kwargs={'pk': self.habit.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(pk=self.habit.pk).exists())


class HabitSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(nickname='testuser', password='password')
        self.useful_habit = UsefulHabit.objects.create(action='Exercise')

    def test_valid_habit_serializer(self):
        habit = Habit.objects.create(
            user=self.user,
            place='Test Place',
            time=timezone.now(),
            time_complete='00:01:00',
            useful_action=self.useful_habit,
            periodicity=1,
            sign_publicity=True
        )
        serializer = HabitSerializer(habit)
        data = serializer.data
        self.assertEqual(data['user'], habit.user.nickname)
        self.assertEqual(data['place'], habit.place)
        self.assertEqual(data['time'], habit.time.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(data['time_complete'], '00:01:00')
        self.assertEqual(data['useful_action_value'], habit.useful_action.action)

    def test_invalid_habit_serializer(self):
        serializer = HabitSerializer(data={
            'user': self.user.nickname,
            'place': 'Test Place',
            'time': timezone.now(),
            'time_complete': '00:01:00',
            'useful_action': None,
            'periodicity': 8,
            'sign_publicity': True
        })
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['useful_action']))
