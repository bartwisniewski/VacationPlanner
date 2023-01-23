from abc import ABC
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db import models


class SingleObjectUserRoleRequiredView(LoginRequiredMixin, UserPassesTestMixin):
    success_url = None
    permission_role = None
    permission_denied_message = f'you are not allowed'

    def test_func(self):
        self.object = self.get_object()
        return self.object.test_user_role(self.request.user, self.permission_role)

    def handle_no_permission(self):
        messages.warning(self.request, self.permission_denied_message)
        return HttpResponseRedirect(self.get_success_url())


def owner_only(method):
    def inner(view, *args, **kwargs):
        if view.object.test_user_role(view.request.user, 'owner'):
            method(view, *args, **kwargs)
        else:
            messages.warning(view.request, "You are not the owner")
    return inner


class MembersUpdateManager(ABC):
    Model = None

    @classmethod
    def __get_member(cls, id: int) -> models.Model:
        try:
            return cls.Model.objects.get(pk=id)
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
    def __member_changed(cls, member_data: dict):
        member = cls.__get_member(member_data.get('id'))
        if member.admin != member_data.get('admin') or member.owner != member_data.get('owner'):
            return True
        return False

    @classmethod
    def update_members(cls, count: int, post_data: dict):
        members_count = count
        for it in range(0, members_count):
            member_data = cls.Model.from_formset_data(post_data, it)
            cls.__update_member(member_data)

    @classmethod
    def members_changed(cls, count: int, post_data: dict):
        members_count = count
        for it in range(0, members_count):
            member_data = cls.Model.from_formset_data(post_data, it)
            if cls.__member_changed(member_data):
                return True
        return False
