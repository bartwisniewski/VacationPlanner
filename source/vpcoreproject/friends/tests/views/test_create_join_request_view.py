from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.messages import constants as message_constants

from friends.models import Friends, JoinRequest


class CreateJoinRequestViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.friends = Friends.objects.create(nickname="Test Group")

        self.url = reverse("create-join-request", args=[self.friends.pk])
        self.login_url = reverse("login")
        self.request_confirm_template_name = "friends/request_confirm.html"

    def test_unauthenticated_user_redirects_to_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{self.login_url}?next={self.url}")

        response = self.client.post(self.url)
        self.assertRedirects(response, f"{self.login_url}?next={self.url}")

    def test_get_request_displays_request_confirm_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.request_confirm_template_name)
        self.assertIn("friends", response.context)
        self.assertEqual(response.context["friends"], self.friends)

    def test_join_request_created_for_post_request(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("friends-list"))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            messages[0].level, message_constants.INFO
        )  # check for "Join request created" message

        # Check that the join request was actually created in the database
        join_requests = JoinRequest.objects.filter(user=self.user, friends=self.friends)
        self.assertEqual(join_requests.count(), 1)
        join_request = join_requests.first()
        self.assertEqual(join_request.user, self.user)
        self.assertEqual(join_request.friends, self.friends)

    def test_multiple_join_requests_are_not_created(self):
        self.client.force_login(self.user)
        # Create a join request for the user and group before
        # attempting to create another one
        JoinRequest.objects.create(user=self.user, friends=self.friends)
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("friends-list"))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            messages[0].level, message_constants.WARNING
        )  # check for "You have already sent a request to join this group" message

        # Check that only one join request exists in the database
        join_requests = JoinRequest.objects.filter(user=self.user, friends=self.friends)
        self.assertEqual(join_requests.count(), 1)
