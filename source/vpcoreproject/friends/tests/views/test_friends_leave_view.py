from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from users.tests.mixins import LoginRequiredViewTest
from friends.tests.data import Generator
from friends.models import UserToFriends


class FriendsLeaveViewTest(LoginRequiredViewTest, TestCase):
    redirect_url = reverse("friends-list")

    def setUp(self):
        super().setUp()
        self.user = self.users[0]
        friends_data = [("friends1",)]
        self.friends_generator = Generator()
        self.friends = self.friends_generator.generate_friends(friends_data)
        self.tested_friends = self.friends[0]
        self.user_to_friends = [
            self.friends_generator.add_user(
                friends=self.tested_friends, user=self.user, admin=True, owner=False
            ),
            self.friends_generator.add_user(
                friends=self.tested_friends, user=self.users[1], admin=True, owner=True
            ),
        ]
        self.tested_relation = self.user_to_friends[0]
        self.url = reverse("friends-leave", kwargs={"pk": self.tested_friends.id})

    def test_should_return_action_on_get(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(self.url)
        self.assertIn("action", response.context.keys())

    def test_should_return_object_on_get(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(self.url)
        object = response.context.get("object")
        self.assertEqual(object.id, self.tested_relation.id)

    def test_should_delete_relation_on_post(self):
        self.client.login(username=self.user.username, password=self.user.password)
        self.client.post(self.url)
        self.assertRaises(
            ObjectDoesNotExist, UserToFriends.objects.get, id=self.tested_relation.id
        )

    def test_should_redirect_when_user_not_member(self):
        user = self.users[2]
        self.client.login(username=user.username, password=user.password)
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            self.redirect_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_should_redirect_when_user_is_only_owner(self):
        user = self.users[1]
        self.client.login(username=user.username, password=user.password)
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            self.redirect_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_should_return_ok_when_user_is_not_only_onwer(self):
        self.friends_generator.add_user(
            friends=self.tested_friends, user=self.users[2], admin=True, owner=True
        )
        user = self.users[1]
        self.client.login(username=user.username, password=user.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
