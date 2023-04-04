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
        friends_generator = Generator()
        self.friends = friends_generator.generate_friends()
        friends_generator.add_user(self.friends[0], self.users[0], True, True)
        friends_generator.add_user(self.friends[1], self.users[0], False, False)

    def test_should_contain_all_friends_of_user_as_object_list(self):

        self.client.login(
            username=self.users[0].username, password=self.users[0].password
        )
        response = self.client.get(MyFriendsListViewTest.url)
        errors = []
        if "object_list" not in response.context.keys():
            errors.append("object_list not in context")
        elif len(response.context["object_list"]) != 2:
            errors.append("object_list does not contain all friends")
        assert not errors, "errors occured:\n{}".format("\n".join(errors))
