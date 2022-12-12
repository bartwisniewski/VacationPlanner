from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View, TemplateView
from django.views.generic.edit import CreateView, DeleteView


from events.models import PlaceProposal, PlaceProposalVote, Event, UserToEvent
from events.forms import PlaceProposalForm
from places.models import Place


class PlaceProposalCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = PlaceProposal
    form_class = PlaceProposalForm
    permission_denied_message = f'you are not participant of this event'

    def get_success_url(self):
        event = self.get_event(self.request)
        if event:
            return reverse('event-detail', kwargs={'pk': event.id})
        return reverse('event-list')

    def test_func(self):
        event = self.get_event(self.request)
        return event.test_user(self.request.user)

    def handle_no_permission(self):
        messages.warning(self.request, self.permission_denied_message)
        return HttpResponseRedirect(self.get_success_url())

    def get_event(self, request):
        event_id = self.kwargs['pk']
        return Event.get_or_warning(event_id, request)

    def get_context_data(self, **kwargs):
        event = self.get_event(self.request)
        context = super().get_context_data(**kwargs)
        if event:
            context['event'] = event
        return context

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['place'].queryset = Place.objects.filter(created_by=self.request.user)
        return form
