from django.test import TestCase, Client
from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

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


class LoginRequiredViewTest(object):
    url = ""

    def setUp(self):
        self.client = Client()
        self.users = UserGenerator().generate_users()

    def test_should_return_ok_for_logged_user(self):
        self.client.login(
            username=self.users[0].username, password=self.users[0].password
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_should_redirect_for_unlogged_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{settings.LOGIN_URL}?next={self.url}",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
