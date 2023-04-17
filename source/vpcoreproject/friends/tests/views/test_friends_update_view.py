from django.test import TestCase
from django.urls import reverse

from users.tests.mixins import SingleObjectUserRoleRequiredViewTest
from friends.tests.data import Generator
from friends.models import Friends, UserToFriends


class FriendsUpdateViewTest(SingleObjectUserRoleRequiredViewTest, TestCase):
    redirect_url = reverse("friends-list")

    def setUp(self):
        super().setUp()
        self.user = self.users[0]

        friends_data = [("friends1",)]
        friends_generator = Generator()
        self.friends = friends_generator.generate_friends(friends_data)
        self.tested_friends = self.friends[0]
        self.user_to_friends = [
            friends_generator.add_user(self.tested_friends, self.user, True, True),
            friends_generator.add_user(
                self.tested_friends, self.users[1], False, False
            ),
        ]
        self.allowed_user = self.user
        self.disallowed_user = self.users[1]
        self.url = reverse("friends-edit", kwargs={"pk": self.tested_friends.id})

    def test_should_return_form_on_get(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(self.url)
        self.assertIn("form", response.context.keys())

    def test_should_return_object_on_get(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(self.url)
        object = response.context.get("object")
        self.assertEqual(object.id, self.tested_friends.id)

    def test_should_update_friends_on_post(self):
        self.client.login(username=self.user.username, password=self.user.password)
        friends_data = {"nickname": "updated_friends1"}
        self.client.post(self.url, friends_data)
        self.assertEqual(
            Friends.objects.get(id=self.tested_friends.id).nickname,
            friends_data.get("nickname"),
        )

    def test_should_update_role_on_post(self):
        self.client.login(username=self.user.username, password=self.user.password)
        tested_member = self.user_to_friends[1]
        members_data = {
            "form-TOTAL_FORMS": 1,
            "form-0-id": tested_member.id,
            "form-0-username": tested_member.user.username,
            "form-0-admin": "on",
            "form-0-owner": False,
        }
        self.client.post(self.url, members_data)
        self.assertEqual(UserToFriends.objects.get(id=tested_member.id).admin, True)
