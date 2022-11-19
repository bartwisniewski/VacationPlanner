from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
# Create your views here.

from friends.models import Friends, UserToFriends, JoinRequest


class MyFriendsListView(LoginRequiredMixin, ListView):

    model = Friends
    paginate_by = 10  # if pagination is desired

    def get_queryset(self):
        return Friends.objects.filter(usertofriends__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_requests'] = JoinRequest.objects.filter(user=self.request.user)
        return context


class FriendsCreateView(CreateView):
    model = Friends
    fields = '__all__'
    success_url = reverse_lazy('friends-list')
    # template = friends_form.html

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        UserToFriends(user=self.request.user, friends=self.object, admin=True, owner=True).save()
        return HttpResponseRedirect(self.get_success_url())


# My groups, group of user
# - List of groups
#   -> Create group
#   -> Delete group // Owner
#   -> Edit group // Admin
#   -> Manage requests // Admin
#   -> Leave group // not Owner
# - List of my active requests

# Delete group, post only // Owner

# Edit group // Admin, Owner
# - group name // edit by Admin or Owner
# - group members
#   -> delete member // Admin (only non admins) or Owner
#   -> change admin status // Owner

# Manage requests // Admin
# - list of requests
# -> Accept
# -> Reject

# Find group
# - Search bar
# - List of found groups
# -> Send request
