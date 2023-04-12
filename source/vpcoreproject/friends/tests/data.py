from friends.models import Friends, UserToFriends, JoinRequest
from typing import List


class Generator:
    def __init__(self):
        self.friends = []
        self.user_to_friends = []

    def generate_friends(self, data: List[tuple]):
        for object_data in data:
            obj, created = Friends.objects.get_or_create(nickname=object_data[0])
            if created:
                self.friends.append(obj)
        return self.friends

    def add_user(self, friends, user, admin, owner):
        obj, created = UserToFriends.objects.get_or_create(
            friends=friends, user=user, admin=admin, owner=owner
        )
        if created:
            self.user_to_friends.append(obj)
        return obj

    def make_join_request(self, friends, user):
        obj, created = JoinRequest.objects.get_or_create(friends=friends, user=user)
        if created:
            self.user_to_friends.append(obj)
        return obj
