from events.models import UserToEvent
from members.helpers import MembersUpdateManager


class UserToEventUpdateManager(MembersUpdateManager):
    Model = UserToEvent
