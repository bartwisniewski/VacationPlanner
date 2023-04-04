from django.test import TestCase, Client
from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.urls import reverse

from users.tests.data import users

from events.models import Event, UserToEvent

client = Client()


class LoginRequiredViewTest(TestCase):
    url = ""

    def setUp(self):
        raise NotImplementedError

    def test_should_return_ok_for_logged_user(self):
        client.login(username=users[0].username, password=users[0].password)
        response = self.client.get(self.url)
        client.logout()
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_should_return_forbidden_for_unlogged_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class MyEventListViewTest(LoginRequiredViewTest):
    url = reverse("events-list")

    def setUp(self):
        super().setUp()
