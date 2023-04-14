from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from users.tests.mixins import SingleObjectUserRoleRequiredViewTest
from friends.tests.data import Generator
from friends.models import Friends, UserToFriends


class FriendsDeleteViewTest(SingleObjectUserRoleRequiredViewTest, TestCase):
    redirect_url = reverse("friends-list")

    def setUp(self):
        super().setUp()
        self.user = self.users[0]

        friends_data = [("friends1",)]
        friends_generator = Generator()
        self.friends = friends_generator.generate_friends(friends_data)
        self.tested_friends = self.friends[0]
        self.user_to_friends = [
            friends_generator.add_user(
                friends=self.tested_friends, user=self.user, admin=True, owner=True
            ),
            friends_generator.add_user(
                friends=self.tested_friends, user=self.users[1], admin=True, owner=False
            ),
        ]
        self.allowed_user = self.user
        self.disallowed_user = self.users[1]
        self.url = reverse("friends-delete", kwargs={"pk": self.tested_friends.id})

    def test_should_return_form_on_get(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(self.url)
        self.assertIn("form", response.context.keys())

    def test_should_return_object_on_get(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(self.url)
        object = response.context.get("object")
        self.assertEqual(object.id, self.tested_friends.id)

    def test_should_delete_friends_on_post(self):
        self.client.login(username=self.user.username, password=self.user.password)
        self.client.post(self.url)
        self.assertRaises(
            ObjectDoesNotExist, Friends.objects.get, id=self.tested_friends.id
        )
