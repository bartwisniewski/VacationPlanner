from django.test import TestCase, Client
from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.urls import reverse
client = Client()


class DashboardTest(TestCase):
    url = reverse("dashboard")

    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def test_should_return_ok_for_unlogged_user(self):
        response = self.client.get(DashboardTest.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_should_return_no_joined_in_context_for_unlogged_user(self):
        response = self.client.get(DashboardTest.url)
        self.assertNotIn('joined', response.context)

    def test_should_return_joined_in_context_for_logged_in_user(self):
        client.login(username='temporary', password='temporary')
        response = client.get(DashboardTest.url)
        self.assertIn('joined', response.context)
