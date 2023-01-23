from friends.models import UserToFriends
from members.helpers import MembersUpdateManager


class UserToFriendsUpdateManager(MembersUpdateManager):
    Model = UserToFriends
