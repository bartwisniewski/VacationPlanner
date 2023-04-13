from django.test import TestCase
from django.urls import reverse

from users.tests.mixins import SingleObjectUserRoleRequiredViewTest
from friends.tests.data import Generator


class FriendsUpdateViewTest(SingleObjectUserRoleRequiredViewTest, TestCase):
    redirect_url = reverse("friends-list")

    def setUp(self):
        super().setUp()
        self.user = self.users[0]

        friends_data = [("friends1",)]
        friends_generator = Generator()
        self.friends = friends_generator.generate_friends(friends_data)
        friends_generator.add_user(self.friends[0], self.user, True, True)
        friends_generator.add_user(self.friends[1], self.users[1], False, False)
        self.allowed_user = self.user
        self.disallowed_user = self.users[1]
        self.url = reverse("friends-edit", kwargs={"pk": self.friends[0].id})

    def test_should_return_form_on_get(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(self.url)
        self.assertIn("form", response.context.keys())

    def test_should_return_object_on_get(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(self.url)
        self.assertIn("object", response.context.keys())
