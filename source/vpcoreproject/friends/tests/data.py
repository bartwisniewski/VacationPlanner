from friends.models import Friends, UserToFriends


class Generator:
    data = [("friends1",), ("friends2",), ("friends3",)]

    def __init__(self):
        self.friends = []
        self.user_to_friends = []

    def generate_friends(self):
        for object_data in Generator.data:
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
