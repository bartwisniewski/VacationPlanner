from django.test import TestCase, Client
from django.urls import reverse

from users.tests.mixins import LoginRequiredViewTest
from friends.tests.data import Generator
from friends.models import Friends, UserToFriends


class FriendsUpdateViewTest(LoginRequiredViewTest, TestCase):
    def setUp(self):
        super().setUp()
        self.user = self.users[0]
        friends_data = [("friends1",)]
        friends_generator = Generator()
        self.friends = friends_generator.generate_friends(friends_data)
        friends_generator.add_user(self.friends[0], self.user, True, True)
        self.url = reverse("friends-edit", kwargs={"pk": self.friends[0].id})

    def test_should_return_form_on_get(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(self.url)
        self.assertIn("form", response.context.keys())

    def test_should_return_object_on_get(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(self.url)
        self.assertIn("object", response.context.keys())
