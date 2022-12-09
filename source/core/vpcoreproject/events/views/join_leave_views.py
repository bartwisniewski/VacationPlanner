from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView

from events.models import Event, UserToEvent


class JoinView(TemplateView):
    success_url = reverse_lazy('events-list')
    template_name = "events/join_confirm.html"

    def get(self, request, *args, **kwargs):
        event_id = self.kwargs['pk']
        event = Event.get_or_warning(event_id, request)
        if event:
            context = self.get_context_data(**kwargs)
            context['event'] = event
            return self.render_to_response(context)

        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        event_id = self.kwargs['pk']
        event = Event.get_or_warning(event_id, request)
        if event:
            user = request.user
            user_to_event, created = UserToEvent.objects.get_or_create(user=user, event=event)
            if created:
                messages.info(self.request, f'You have successfully joined event: {event.name}')
            else:
                messages.warning(self.request, f'You are already attending the event: {event.name}')
        return HttpResponseRedirect(self.success_url)


class LeaveView(TemplateView):
    success_url = reverse_lazy('events-list')
    template_name = "events/join_confirm.html"

    def get(self, request, *args, **kwargs):
        event_id = self.kwargs['pk']
        event = Event.get_or_warning(event_id, request)
        if event:
            context = self.get_context_data(**kwargs)
            context['event'] = event
            return self.render_to_response(context)

        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        event_id = self.kwargs['pk']
        event = Event.get_or_warning(event_id, request)
        if event:
            user = request.user
            user_to_event, created = UserToEvent.objects.get_or_create(user=user, event=event)
            if created:
                messages.info(self.request, f'You have successfully joined event: {event.name}')
            else:
                messages.warning(self.request, f'You are already attending the event: {event.name}')
        return HttpResponseRedirect(self.success_url)