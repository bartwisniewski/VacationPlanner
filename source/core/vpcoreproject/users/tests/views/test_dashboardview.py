from http import HTTPStatus

from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth import login, get_user_model

client = Client()


class TestDashboardView(TestCase):
    url = reverse("dashboard")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User = get_user_model()
        user = User.objects.create_user(username='temporary', password='temporary')

    def test_should_response_200_and_no_joined_if_not_logged_in(self):

        response = client.get(TestDashboardView.url)
        context = response.context

        self.assertEqual(first=response.status_code, second=HTTPStatus.OK)
        self.assertNotIn('joined', context)

    def test_should_response_200_and_joined_in_context_if_logged_in(self):
        client.login(username='temporary', password='temporary')
        response = client.get(TestDashboardView.url)
        context = response.context

        self.assertEqual(first=response.status_code, second=HTTPStatus.OK)
        self.assertIn('joined', context)
