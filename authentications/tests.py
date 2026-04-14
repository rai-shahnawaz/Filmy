from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from authentications.serializers import RegisterSerializer


class RegisterSerializerTests(TestCase):
    def test_serializer_rejects_mismatched_passwords(self):
        serializer = RegisterSerializer(
            data={
                "username": "rai",
                "email": "rai@example.com",
                "first_name": "Rai",
                "last_name": "Shahnawaz",
                "password": "StrongPass123!",
                "password2": "DifferentPass123!",
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_serializer_creates_user(self):
        serializer = RegisterSerializer(
            data={
                "username": "filmy-user",
                "email": "filmy@example.com",
                "first_name": "Filmy",
                "last_name": "User",
                "password": "StrongPass123!",
                "password2": "StrongPass123!",
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, "filmy-user")
        self.assertTrue(user.check_password("StrongPass123!"))


class AuthenticationUrlTests(TestCase):
    def test_register_url_is_available(self):
        self.assertEqual(reverse("register"), "/api/register/")
