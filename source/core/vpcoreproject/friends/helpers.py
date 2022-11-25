from django.contrib import messages
from friends.models import UserToFriends
from django.core.exceptions import ObjectDoesNotExist


def owner_only(method):
    def inner(view, *args, **kwargs):
        if view.object.test_user_role(view.request.user, 'owner'):
            method(view, *args, **kwargs)
        else:
            messages.warning(view.request, "You are not the owner")
    return inner


class UserToFriendsUpdateManager:

    @classmethod
    def __get_member(cls, id: int) -> UserToFriends:
        try:
            return UserToFriends.objects.get(pk=id)
        except ObjectDoesNotExist:
            pass
        return None

    @classmethod
    def __update_member(cls, member_data: dict):
        member = cls.__get_member(member_data.get('id'))
        if member and not member.owner:
            member.admin = member_data.get('admin')
            member.owner = member_data.get('owner')
            member.save()

    @classmethod
    def update_members(cls, count: int, post_data: dict):
        members_count = count
        for it in range(0, members_count):
            member_data = UserToFriends.from_formset_data(post_data, it)
            cls.__update_member(member_data)
