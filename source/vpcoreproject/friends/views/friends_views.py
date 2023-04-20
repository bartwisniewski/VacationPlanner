from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from friends.models import Friends, UserToFriends, JoinRequest
from friends.helpers import UserToFriendsUpdateManager
from members.helpers import SingleObjectUserRoleRequiredView, owner_only
from chat.views import ChatMixin


class MyFriendsListView(LoginRequiredMixin, ListView, ChatMixin):
    model = Friends
    paginate_by = 10

    def get_queryset(self):
        return Friends.objects.filter(usertofriends__user=self.request.user).order_by(
            "nickname"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_requests"] = JoinRequest.objects.filter(user=self.request.user)
        my_admin_groups = self.object_list.filter(usertofriends__admin=True)
        context["other_requests"] = JoinRequest.objects.filter(
            friends__in=my_admin_groups
        )
        self.add_chat_context(context, self.request)
        return context


class FriendsCreateView(LoginRequiredMixin, CreateView):
    model = Friends
    fields = "__all__"
    success_url = reverse_lazy("friends-list")

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        UserToFriends(
            user=self.request.user, friends=self.object, admin=True, owner=True
        ).save()
        return HttpResponseRedirect(self.get_success_url())


class FriendsUpdateView(SingleObjectUserRoleRequiredView, UpdateView):
    model = Friends
    fields = "__all__"
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("friends-list")
    permission_role = "admin"
    permission_denied_message = (
        f"you are not {permission_role} of this group of friends"
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        related_users = self.object.usertofriends_set.all()
        context["users"] = related_users
        formset = self.object.get_users_formset()
        context["users_formset"] = formset
        return context

    @owner_only
    def update_members(self, request, *args, **kwargs):
        count = int(request.POST.get("form-TOTAL_FORMS", 0))
        post_data = request.POST
        UserToFriendsUpdateManager.update_members(count, post_data)

    def post(self, request, *args, **kwargs):
        self.update_members(request, *args, **kwargs)
        return super().post(request, *args, **kwargs)


class FriendsDeleteView(SingleObjectUserRoleRequiredView, DeleteView):
    model = Friends
    permission_role = "owner"
    permission_denied_message = (
        f"you are not {permission_role} of this group of friends"
    )
    success_url = reverse_lazy("friends-list")


class UserToFriendsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserToFriends
    permission_denied_message = "you are not permited to delete this member"
    success_url = reverse_lazy("friends-list")

    def test_func(self):
        self.object = self.get_object()
        friends_group = self.object.friends
        deleted_is_admin = self.object.admin
        deleted_is_owner = self.object.owner
        user_is_admin = friends_group.test_user_role(self.request.user, "admin")
        user_is_owner = friends_group.test_user_role(self.request.user, "owner")

        return (user_is_admin and not deleted_is_admin) or (
            user_is_owner and not deleted_is_owner
        )

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.warning(self.request, self.permission_denied_message)
        return HttpResponseRedirect(self.get_success_url())


class FriendsLeaveView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    success_url = reverse_lazy("friends-list")
    permission_denied_message = (
        "you cannot leave your own group if there is no other owner"
    )
    template_name = "friends/confirm.html"

    def get_object(self, request, *args, **kwargs):
        friends_id = self.kwargs["pk"]
        friends = Friends.get_or_warning(id=friends_id, request=request)
        if friends:
            user = request.user
            return UserToFriends.get_or_warning(
                user=user, friends=friends, request=request
            )
        return None

    def get(self, request, *args, **kwargs):
        user_to_friends = self.get_object(request, *args, **kwargs)
        if user_to_friends:
            context = self.get_context_data(**kwargs)
            context["object"] = user_to_friends.friends
            context["action"] = "leave"
            return self.render_to_response(context)

        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        user_to_friends = self.get_object(request, *args, **kwargs)
        if user_to_friends:
            user_to_friends.delete()
            messages.info(self.request, "You have left the group")
        return HttpResponseRedirect(self.success_url)

    def test_func(self):
        self.object = self.get_object(self.request)
        if not self.object:
            return False
        friends_group = self.object.friends
        user_is_owner = friends_group.test_user_role(self.request.user, "owner")
        other_owners = friends_group.usertofriends_set.filter(owner=True).exclude(
            user=self.request.user
        )
        return not user_is_owner or other_owners.count()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.warning(self.request, self.permission_denied_message)
        return HttpResponseRedirect(self.success_url)
