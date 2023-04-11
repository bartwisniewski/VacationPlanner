from django.test import TestCase, Client
from http import HTTPStatus
from django.urls import reverse

from users.tests.data import UserGenerator


class DashboardTest(TestCase):
    url = reverse("dashboard")

    def setUp(self):
        self.client = Client()
        self.users = UserGenerator().generate_users()

    def test_should_return_ok_for_unlogged_user(self):
        self.client.logout()
        response = self.client.get(DashboardTest.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_should_return_no_joined_in_context_for_unlogged_user(self):
        self.client.logout()
        response = self.client.get(DashboardTest.url)
        self.assertNotIn("joined", response.context)

    def test_should_return_joined_in_context_for_logged_in_user(self):
        self.client.login(
            username=self.users[0].username, password=self.users[0].password
        )
        response = self.client.get(DashboardTest.url)
        self.assertIn("joined", response.context)
