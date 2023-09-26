from django.test import TestCase
from django.urls import reverse
from friends.tests.data import Generator
from users.tests.mixins import LoginRequiredViewTest


class MyFriendsListViewTest(LoginRequiredViewTest, TestCase):
    url = reverse("friends-list")

    def setUp(self):
        super().setUp()
        self.user = self.users[0]
        friends_data = [("friends1",), ("friends2",), ("friends3",), ("friends4",)]
        friends_generator = Generator()
        self.friends = friends_generator.generate_friends(friends_data)
        user_friends_config = [
            (self.friends[0], self.user, True, True),
            (self.friends[1], self.user, False, False),
        ]
        self.user_to_friends = []
        for config in user_friends_config:
            self.user_to_friends.append(friends_generator.add_user(*config))
        self.join_requests = [
            friends_generator.make_join_request(self.friends[0], self.users[1]),
            friends_generator.make_join_request(self.friends[0], self.users[2]),
            friends_generator.make_join_request(self.friends[1], self.users[1]),
            friends_generator.make_join_request(self.friends[1], self.users[2]),
            friends_generator.make_join_request(self.friends[2], self.user),
            friends_generator.make_join_request(self.friends[3], self.user),
        ]

    def test_should_contain_object_list(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(MyFriendsListViewTest.url)
        self.assertIn("object_list", response.context.keys())

    def test_should_contain_my_requests(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(MyFriendsListViewTest.url)
        self.assertIn("my_requests", response.context.keys())

    def test_should_contain_other_requests(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(MyFriendsListViewTest.url)
        self.assertIn("other_requests", response.context.keys())

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

    def test_should_contain_all_my_join_requests(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(MyFriendsListViewTest.url)
        expected = {self.join_requests[4].id, self.join_requests[5].id}
        response_requests = response.context.get("my_requests", [])
        response_requests_ids = set([rr.id for rr in response_requests])
        self.assertEqual(response_requests_ids, expected)

    def test_should_contain_all_other_requests_where_user_is_admin(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(MyFriendsListViewTest.url)
        expected = {self.join_requests[0].id, self.join_requests[1].id}
        response_requests = response.context.get("other_requests", [])
        response_requests_ids = set([rr.id for rr in response_requests])
        self.assertEqual(response_requests_ids, expected)
