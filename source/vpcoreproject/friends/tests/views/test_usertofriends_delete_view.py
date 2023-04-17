from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from users.tests.mixins import LoginRequiredViewTest
from friends.tests.data import Generator
from friends.models import Friends, UserToFriends


class UserToFriendsDeleteViewTest(LoginRequiredViewTest, TestCase):
    url_name = "friends-member-delete"
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
                friends=self.tested_friends, user=self.users[1], admin=True, owner=True
            ),
            friends_generator.add_user(
                friends=self.tested_friends, user=self.users[2], admin=True, owner=False
            ),
            friends_generator.add_user(
                friends=self.tested_friends, user=self.users[3], admin=True, owner=False
            ),
            friends_generator.add_user(
                friends=self.tested_friends,
                user=self.users[4],
                admin=False,
                owner=False,
            ),
        ]
        self.deleted_member = self.user_to_friends[4]
        self.url = reverse(
            UserToFriendsDeleteViewTest.url_name, kwargs={"pk": self.deleted_member.id}
        )

    def test_should_return_form_on_get(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(self.url)
        self.assertIn("form", response.context.keys())

    def test_should_return_object_on_get(self):
        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get(self.url)
        object = response.context.get("object")
        self.assertEqual(object.id, self.deleted_member.id)

    def test_should_delete_friends_on_post(self):
        self.client.login(username=self.user.username, password=self.user.password)
        self.client.post(self.url)
        self.assertRaises(
            ObjectDoesNotExist, UserToFriends.objects.get, id=self.deleted_member.id
        )

    def test_should_redirect_when_admin_deletes_admin(self):
        user = self.users[2]
        self.deleted_member = self.user_to_friends[3]
        self.url = reverse(
            UserToFriendsDeleteViewTest.url_name, kwargs={"pk": self.deleted_member.id}
        )
        self.client.login(username=user.username, password=user.password)
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            self.redirect_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_should_redirect_when_admin_deletes_owner(self):
        user = self.users[2]
        self.deleted_member = self.user_to_friends[1]
        self.url = reverse(
            UserToFriendsDeleteViewTest.url_name, kwargs={"pk": self.deleted_member.id}
        )
        self.client.login(username=user.username, password=user.password)
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            self.redirect_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_should_redirect_when_owner_deletes_owner(self):
        user = self.users[0]
        self.deleted_member = self.user_to_friends[1]
        self.url = reverse(
            UserToFriendsDeleteViewTest.url_name, kwargs={"pk": self.deleted_member.id}
        )
        self.client.login(username=user.username, password=user.password)
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            self.redirect_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_should_redirect_when_user_not_admin_or_owner(self):
        user = self.users[4]
        self.deleted_member = self.user_to_friends[3]
        self.url = reverse(
            UserToFriendsDeleteViewTest.url_name, kwargs={"pk": self.deleted_member.id}
        )
        self.client.login(username=user.username, password=user.password)
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            self.redirect_url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_should_return_ok_when_admin_deletes_regular(self):
        user = self.users[3]
        self.deleted_member = self.user_to_friends[4]
        self.url = reverse(
            UserToFriendsDeleteViewTest.url_name, kwargs={"pk": self.deleted_member.id}
        )
        self.client.login(username=user.username, password=user.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_should_return_ok_when_owner_deletes_admin(self):
        user = self.users[0]
        self.deleted_member = self.user_to_friends[2]
        self.url = reverse(
            UserToFriendsDeleteViewTest.url_name, kwargs={"pk": self.deleted_member.id}
        )
        self.client.login(username=user.username, password=user.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
