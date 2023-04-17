from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from friends.models import Friends, UserToFriends


class FriendsFindViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("friends-find")
        self.user1 = get_user_model().objects.create_user(
            username="testuser1", password="testpass1"
        )
        self.user2 = get_user_model().objects.create_user(
            username="testuser2", password="testpass2"
        )
        self.friend1 = Friends.objects.create(nickname="friend1")
        self.friend2 = Friends.objects.create(nickname="friend2")
        self.friend3 = Friends.objects.create(nickname="friend3")
        UserToFriends.objects.create(user=self.user1, friends=self.friend1)
        UserToFriends.objects.create(user=self.user2, friends=self.friend2)

    def test_friends_find_view_with_no_query_param(self):
        self.client.login(username="testuser1", password="testpass1")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "friends/friends_find.html")
        self.assertQuerysetEqual(
            response.context["object_list"], [self.friend3, self.friend2]
        )

    def test_friends_find_view_with_query_param(self):
        self.client.login(username="testuser1", password="testpass1")
        response = self.client.get(self.url, {"q": "friend2"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "friends/friends_find.html")
        self.assertQuerysetEqual(response.context["object_list"], [self.friend2])
        self.assertEqual(response.context["phrase"], "friend2")

    def test_friends_find_view_with_short_query_param(self):
        self.client.login(username="testuser1", password="testpass1")
        response = self.client.get(self.url, {"q": "f"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "friends/friends_find.html")
        messages = list(response.context.get("messages"))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Search phrase too short min 3 characters")

    def test_friends_find_view_with_post_request(self):
        self.client.login(username="testuser1", password="testpass1")
        response = self.client.post(self.url, {"phrase": "friend1"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"{self.url}?q=friend1")
