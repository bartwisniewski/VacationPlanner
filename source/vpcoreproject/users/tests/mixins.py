from django.test import Client
from http import HTTPStatus

from django.conf import settings
from users.tests.data import UserGenerator


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
