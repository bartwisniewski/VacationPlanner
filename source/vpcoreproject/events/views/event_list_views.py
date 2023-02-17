from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from events.models import Event, UserToEvent
from chat.views import ChatMixin


class MyEventsListView(LoginRequiredMixin, ListView, ChatMixin):

    model = Event
    paginate_by = 10

    def get_queryset(self):
        return Event.filter_by_user(self.request.user).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_events = Event.filter_by_user(self.request.user)
        my_friends_events = Event.user_friends_events(self.request.user)
        context["friends_events"] = my_friends_events.difference(my_events).order_by(
            "-id"
        )
        self.add_chat_context(context, self.request)
        return context
