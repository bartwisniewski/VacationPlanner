from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from events.models import Event, UserToEvent
from friends.models import Friends
# Create your views here.


class MyEventsListView(LoginRequiredMixin, ListView):

    model = Event
    paginate_by = 10

    def get_queryset(self):
        return Event.user_events(self.request.user).order_by('-id')


class MissingEventsListView(LoginRequiredMixin, ListView):

    model = Event
    paginate_by = 10

    def get_queryset(self):
        my_friends_events = Event.objects.filter(friends__usertofriends__user=self.request.user)
        my_events = Event.user_events(self.request.user)
        missing_events = my_friends_events.difference(my_events)
        return missing_events.order_by('-id')


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['name', 'friends', ]
    success_url = reverse_lazy('events-list')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['friends'].queryset = Friends.objects.filter(usertofriends__user=self.request.user)
        return form

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        UserToEvent(user=self.request.user, event=self.object, admin=True, owner=True).save()
        return HttpResponseRedirect(self.get_success_url())
