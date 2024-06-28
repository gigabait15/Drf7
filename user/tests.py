from django.db import IntegrityError
from django.test import TestCase
from user.models import User
from user.serializers import UserRegistrationSerializer


class UserManagerTests(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(nickname='testuser', password='password')
        self.assertEqual(user.nickname, 'testuser')
        self.assertTrue(user.check_password('password'))
        self.assertEqual(str(user), 'testuser')

        with self.assertRaises(ValueError):
            User.objects.create_user(nickname='', password='password')

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(nickname='admin', password='adminpassword')
        self.assertEqual(superuser.nickname, 'admin')
        self.assertEqual(str(superuser), 'admin')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_str_representation(self):
        user = User.objects.create_user(nickname='testuser', password='password')
        self.assertEqual(str(user), 'testuser')

    def test_unique_nickname_constraint(self):
        User.objects.create_user(nickname='testuser', password='password')

        with self.assertRaises(IntegrityError):
            User.objects.create_user(nickname='testuser', password='password')

    def test_tg_id_default_value(self):
        user = User.objects.create_user(nickname='testuser', password='password')
        self.assertEqual(user.tg_id, 503234730)


class UserRegistrationSerializerTests(TestCase):

    def test_create_user(self):
        data = {
            'nickname': 'testuser',
            'password': 'password123'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.nickname, 'testuser')
        self.assertTrue(user.check_password('password123'))

    def test_create_user_invalid_data(self):
        data = {
            'nickname': '',
            'password': 'password123'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('nickname', serializer.errors)

    def test_create_user_missing_password(self):
        data = {
            'nickname': 'testuser'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
