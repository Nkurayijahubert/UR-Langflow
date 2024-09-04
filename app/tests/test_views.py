from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from unittest.mock import patch

User = get_user_model()

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_register_view_success(self):
        data = {'username': 'newuser', 'password': 'newpassword'}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_view_failure(self):
        data = {'username': 'newuser'}  # Missing password
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)