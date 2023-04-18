from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from friends.models import Friends, JoinRequest, UserToFriends
from django.contrib.messages import get_messages
from django.contrib.messages import constants as message_constants


class AnswerJoinRequestViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("answer-join-request", args=[1])
        self.login_url = reverse("login")
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.user2 = get_user_model().objects.create_user(
            username="testuser2", password="testpass"
        )
        self.friends = Friends.objects.create(nickname="Test Friends")
        UserToFriends.objects.create(
            friends=self.friends, user=self.user, admin=True, owner=True
        )
        self.join_request = JoinRequest.objects.create(
            user=self.user2, friends=self.friends
        )

    def test_unauthenticated_user_redirects_to_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{self.login_url}?next={self.url}")

        response = self.client.post(self.url)
        self.assertRedirects(response, f"{self.login_url}?next={self.url}")

    def test_no_admin_user_redirects(self):
        self.client.force_login(self.user2)
        self.url = reverse("answer-join-request", args=[1])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("friends-list"))

    def test_get(self):
        self.client.force_login(self.user)
        self.url = reverse("answer-join-request", args=[100])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("friends-list"))

        self.url = reverse("answer-join-request", args=[1])
        response = self.client.get(self.url + "?accept=true")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "friends/confirm.html")
        action = response.context["action"]
        self.assertEqual(action, "accept")
        join_request = self.join_request
        context_join_request = response.context["object"]
        self.assertEqual(join_request.id, context_join_request.id)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        action = response.context["action"]
        self.assertEqual(action, "reject")

    def test_post_accept(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url + "?accept=True")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("friends-list"))
        self.assertEqual(
            UserToFriends.objects.filter(user=self.user2, friends=self.friends).count(),
            1,
        )
        self.assertFalse(
            JoinRequest.objects.filter(user=self.user2, friends=self.friends).exists()
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            messages[0].level, message_constants.INFO
        )  # check for "Join request accepted" message

    def test_post_reject(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url + "?accept=False")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("friends-list"))
        self.assertFalse(
            UserToFriends.objects.filter(user=self.user2, friends=self.friends).exists()
        )
        self.assertFalse(
            JoinRequest.objects.filter(user=self.user2, friends=self.friends).exists()
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            messages[0].level, message_constants.INFO
        )  # check for "Join request accepted" message
