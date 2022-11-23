from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

from friends.models import Friends, UserToFriends, JoinRequest


class FriendsListView(LoginRequiredMixin, ListView):
    template_name_suffix = '_find'
    model = Friends
    paginate_by = 10  # if pagination is desired

    def get_queryset(self):
        phrase = self.request.GET.get('q', '')
        queryset = Friends.objects.exclude(usertofriends__user=self.request.user).order_by('-id')
        if len(phrase) >= 3:
            queryset = queryset.filter(nickname__contains=phrase)
        return queryset


class MyFriendsListView(LoginRequiredMixin, ListView):

    model = Friends
    paginate_by = 10  # if pagination is desired

    def get_queryset(self):
        return Friends.objects.filter(usertofriends__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_requests'] = JoinRequest.objects.filter(user=self.request.user)
        my_admin_groups = self.object_list.filter(usertofriends__admin=True)
        context['other_requests'] = JoinRequest.objects.filter(friends__in=my_admin_groups)
        return context


class FriendsCreateView(LoginRequiredMixin, CreateView):
    model = Friends
    fields = '__all__'
    success_url = reverse_lazy('friends-list')
    # template = friends_form.html

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        UserToFriends(user=self.request.user, friends=self.object, admin=True, owner=True).save()
        return HttpResponseRedirect(self.get_success_url())


class FriendsSingleObjectView(LoginRequiredMixin, UserPassesTestMixin):
    success_url = reverse_lazy('friends-list')
    permission_role = 'admin'
    permission_denied_message = f'you are not {permission_role} of this group of friends'

    def test_func(self):
        self.object = self.get_object()
        return self.object.test_user_role(self.request.user, self.permission_role)

    def handle_no_permission(self):
        messages.warning(self.request, self.permission_denied_message)
        return HttpResponseRedirect(self.get_success_url())


class FriendsUpdateView(FriendsSingleObjectView, UpdateView):
    model = Friends
    fields = '__all__'
    template_name_suffix = '_update_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        related_users = self.object.usertofriends_set.all()
        context['users'] = related_users
        formset = self.object.get_users_formset()
        context['users_formset'] = formset
        return context

    def post(self, request, *args, **kwargs):
        if self.object.test_user_role(self.request.user, 'owner'):
            count = int(request.POST.get('form-TOTAL_FORMS', 0))
            post_data = request.POST
            UserToFriends.update_members(count, post_data)

        return super().post(request, *args, **kwargs)


class FriendsDeleteView(FriendsSingleObjectView,  DeleteView):
    model = Friends
    permission_role = 'owner'
    permission_denied_message = f'you are not {permission_role} of this group of friends'


class UserToFriendsDeleteView(LoginRequiredMixin,  DeleteView):
    model = UserToFriends
    permission_denied_message = f'you are not permited to delete this member'
    success_url = reverse_lazy('friends-list')

    def test_func(self):
        self.object = self.get_object()
        friends_group = self.object.friends
        deleted_is_admin = self.object.admin
        user_is_admin = friends_group.test_user_role(self.request.user, 'admin')
        user_is_owner = friends_group.test_user_role(self.request.user, 'owner')

        return user_is_admin and not deleted_is_admin or user_is_owner

    def handle_no_permission(self):
        messages.warning(self.request, self.permission_denied_message)
        return HttpResponseRedirect(self.get_success_url())


class CreateJoinRequestView(TemplateView):
    success_url = reverse_lazy('friends-list')
    template_name = "friends/request_confirm.html"

    def get(self, request, *args, **kwargs):
        friends_id = self.kwargs['pk']
        try:
            friends = Friends.objects.get(id=friends_id)
            context = self.get_context_data(**kwargs)
            context['friends'] = friends
            return self.render_to_response(context)
        except ObjectDoesNotExist:
            messages.warning(self.request, f'Friends group with id {friends_id} does not exist')
        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        friends_id = self.kwargs['pk']
        try:
            friends = Friends.objects.get(id=friends_id)
            user = request.user
            join_request, created = JoinRequest.objects.get_or_create(user=user, friends=friends)
            if created:
                messages.info(self.request, f'Join request created')
            else:
                messages.warning(self.request, f'You have already sent a request to join this group')
        except ObjectDoesNotExist:
            messages.warning(self.request, f'Friends group with id {friends_id } does not exist')

        return HttpResponseRedirect(self.success_url)


class AnswerJoinRequestView(TemplateView):
    success_url = reverse_lazy('friends-list')
    template_name = "friends/confirm.html"

    def get_object(self):
        request_id = self.kwargs['pk']
        try:
            return JoinRequest.objects.get(id=request_id)
        except ObjectDoesNotExist:
            messages.warning(self.request, f'Join request does not exist')
            return None

    def get(self, request, *args, **kwargs):
        join_request = self.get_object()
        if join_request:
            accept = self.request.GET.get('accept', False)

            context = self.get_context_data(**kwargs)
            context['object'] = join_request
            context['action'] = 'accept' if accept else 'reject'
            return self.render_to_response(context)

        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        join_request = self.get_object()
        if join_request:
            accept = self.request.GET.get('accept', False)
            if accept:
                UserToFriends(user=join_request.user, friends=join_request.friends).save()
                messages.info(self.request, f'Join request accepted')
            else:
                messages.info(self.request, f'Join request rejected')
            join_request.delete()

        return HttpResponseRedirect(self.success_url)

# My groups, group of user
# - List of groups

#   -> Leave group // not Owner

# Delete group, post only // Owner

# Find group
# - Search bar
