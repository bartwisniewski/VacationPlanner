from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView

from events.models import Event


class EventConfrimBookingView(UserPassesTestMixin, TemplateView):
    model = Event
    template_name = "events/booking_confirm.html"
    permission_denied_message = f"you are not promoter of this event"

    def get_object(self):
        object_id = self.kwargs["pk"]
        object_instance = self.model.get_or_warning(object_id, self.request)
        self.object = object_instance

    def get_target_url(self):
        if self.object:
            event = self.object
            return reverse("event-detail", kwargs={"pk": event.id})
        return reverse("event-list")

    def test_func(self):
        self.get_object()
        event = self.object
        return (
            event.status == Event.EventStatus.BOOKING
            and self.request.user == event.promoter
        )

    def handle_no_permission(self):
        messages.warning(self.request, self.permission_denied_message)
        return HttpResponseRedirect(self.get_target_url())

    def get(self, request, *args, **kwargs):
        self.get_object()
        if self.object and self.object.status > 0:
            context = self.get_context_data(**kwargs)
            context["object"] = self.object
            return self.render_to_response(context)
        target_url = self.get_target_url()
        return HttpResponseRedirect(target_url)

    def post_action(self):
        self.object.status = Event.EventStatus.CONFIRMED
        self.object.save()

    def post(self, request, *args, **kwargs):
        self.get_object()
        target_url = self.get_target_url()
        if not self.object:
            return HttpResponseRedirect(target_url)

        self.post_action()

        return HttpResponseRedirect(target_url)
