from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, DeleteView
from django.core.exceptions import ObjectDoesNotExist

from events.models import DateProposal, Event, UserToEvent
from events.forms import DateProposalForm


class DateProposalCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = DateProposal
    form_class = DateProposalForm
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

    def get(self, request, *args, **kwargs):
        event = self.get_event(request)
        if event:
            return super().get(request, *args, **kwargs)

        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        event = self.get_event(self.request)
        context = super().get_context_data(**kwargs)
        if event:
            context['event'] = event

        return context

    def post(self, request, *args, **kwargs):
        event = self.get_event(self.request)
        user_event = UserToEvent.get_or_warning(request.user, event, request)
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, user_event)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, user_event):
        """If the form is valid, save the associated model."""
        form.instance.user_event = user_event
        self.object = form.save()
        return super().form_valid(form)


class DateProposalDeleteView(UserPassesTestMixin, DeleteView):
    model = DateProposal
    permission_denied_message = f'you can only delete your own proposal'

    def get_success_url(self):
        event = self.get_object().user_event.event
        if event:
            return reverse('event-detail', kwargs={'pk': event.id})
        return reverse('event-list')

    def test_func(self):
        return self.request.user == self.get_object().user_event.user

    def handle_no_permission(self):
        messages.warning(self.request, self.permission_denied_message)
        redirect_url = self.get_success_url()
        return HttpResponseRedirect(redirect_url)

