from django.test import TestCase
from django.urls import reverse

from users.tests.mixins import LoginRequiredViewTest
from friends.models import Friends, UserToFriends


class FriendsCreateViewTest(LoginRequiredViewTest, TestCase):
    url = reverse("friends-create")

    def setUp(self):
        super().setUp()
        self.user = self.users[0]

    def test_should_return_form_on_get(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(FriendsCreateViewTest.url)
        self.assertIn("form", response.context.keys())

    def test_creates_friends_on_post(self):
        self.client.login(username=self.user.username, password=self.user.password)
        friends_data = {"nickname": "test_friends"}
        self.client.post(FriendsCreateViewTest.url, friends_data)
        self.assertEqual(Friends.objects.last().nickname, friends_data.get("nickname"))

    def test_creates_user_to_friends_on_post(self):
        self.client.login(username=self.user.username, password=self.user.password)
        friends_data = {"nickname": "test_friends"}
        self.client.post(FriendsCreateViewTest.url, friends_data)

        last = UserToFriends.objects.last()
        last_dict = {
            "friends": last.friends.nickname,
            "user": last.user,
            "admin": last.admin,
            "owner": last.owner,
        }
        expected = {
            "friends": friends_data.get("nickname"),
            "user": self.user,
            "admin": True,
            "owner": True,
        }

        self.assertEqual(last_dict, expected)

    def test_redirects_after_post(self):
        success_url = reverse("friends-list")
        self.client.login(username=self.user.username, password=self.user.password)
        friends_data = {"nickname": "test_friends"}
        response = self.client.post(FriendsCreateViewTest.url, friends_data)
        self.assertRedirects(
            response,
            success_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
