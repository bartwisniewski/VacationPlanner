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
from events.views.date_proposal_views import ProposalVoteView, ProposalUnvoteView, ProposalAcceptView


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
        event = self.get_event(self.request)
        proposals = PlaceProposal.objects.filter(user_event__event=event)
        form.fields['place'].queryset = Place.objects.filter(created_by=self.request.user).exclude(placeproposal__in=proposals)
        return form

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        event = self.get_event(self.request)
        user = self.request.user
        user_event = UserToEvent.get_or_warning(user, event, self.request)
        if user_event:
            form.instance.user_event = user_event
            return super().form_valid(form)
        return super().form_invalid(form)


class PlaceProposalDeleteView(UserPassesTestMixin, DeleteView):
    model = PlaceProposal
    template_name = "events/proposal_confirm_delete.html"
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


class PlaceProposalVoteView(ProposalVoteView):
    proposal_model = PlaceProposal
    vote_model = PlaceProposalVote


class PlaceProposalUnvoteView(ProposalUnvoteView):
    model = PlaceProposalVote


class PlaceProposalAcceptView(ProposalAcceptView):
    model = PlaceProposal

    def post_action(self):
        event = self.object.user_event.event
        event.place = self.object.place
        event.status = Event.EventStatus.BOOKING
        event.save()
