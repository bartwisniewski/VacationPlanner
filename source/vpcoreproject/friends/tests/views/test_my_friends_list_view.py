from django.test import TestCase, Client
from http import HTTPStatus
from django.urls import reverse

from users.tests.views.tests import LoginRequiredViewTest

from friends.tests.data import Generator

client = Client()


class MyFriendsListViewTest(LoginRequiredViewTest, TestCase):
    url = reverse("friends-list")

    def setUp(self):
        super().setUp()
        self.user = self.users[0]
        friends_generator = Generator()
        self.friends = friends_generator.generate_friends()
        user_friends_config = [
            (self.friends[0], self.user, True, True),
            (self.friends[1], self.user, False, False),
        ]
        self.user_to_friends = []
        for config in user_friends_config:
            self.user_to_friends.append(friends_generator.add_user(*config))

    def test_should_contain_object_list(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(MyFriendsListViewTest.url)
        self.assertIn("object_list", response.context.keys())

    def test_should_contain_all_users_friends_groups(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(MyFriendsListViewTest.url)
        my_friends_ids = set([relation.friends.id for relation in self.user_to_friends])
        response_friends = response.context.get("object_list", [])
        response_friends_ids = set([f.id for f in response_friends])
        self.assertEqual(response_friends_ids, my_friends_ids)

    def test_should_not_contain_other_friends_groups(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(MyFriendsListViewTest.url)
        my_friends_ids = set([relation.friends.id for relation in self.user_to_friends])
        all_friends_ids = set([f.id for f in self.friends])
        other_friends_ids = all_friends_ids - my_friends_ids
        friends = response.context.get("object_list", [])
        response_friends_ids = set([f.id for f in friends])
        self.assertTrue(response_friends_ids.isdisjoint(other_friends_ids))
