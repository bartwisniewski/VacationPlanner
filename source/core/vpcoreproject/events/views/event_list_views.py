from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from events.models import Event, UserToEvent


class MyEventsListView(LoginRequiredMixin, ListView):

    model = Event
    paginate_by = 10

    def get_queryset(self):
        return Event.user_events(self.request.user).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_events = Event.user_events(self.request.user)
        my_friends_events = Event.user_friends_events(self.request.user)
        context["friends_events"] = my_friends_events.difference(my_events).order_by(
            "-id"
        )
        return context


class MissingEventsListView(LoginRequiredMixin, ListView):

    model = Event
    paginate_by = 10

    def get_queryset(self):
        my_friends_events = Event.objects.filter(
            friends__usertofriends__user=self.request.user
        )
        my_events = Event.user_events(self.request.user)
        missing_events = my_friends_events.difference(my_events)
        return missing_events.order_by("-id")
