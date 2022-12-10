from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect

from events.models import Event, UserToEvent, DateProposal, DateProposalVote


class EventDetailView(UserPassesTestMixin, DetailView):
    model = Event
    template_suffix_from_status = ["_detail", "_detail_1", "_detail_2"]
    success_url = reverse_lazy('events-list')
    permission_denied_message = f'you are not participant of this event'

    def get_event(self, request):
        event_id = self.kwargs['pk']
        return Event.get_or_warning(event_id, request)

    def test_func(self):
        event = self.get_event(self.request)
        return event.test_user(self.request.user)

    def handle_no_permission(self):
        messages.warning(self.request, self.permission_denied_message)
        return HttpResponseRedirect(EventDetailView.success_url)

    def get_template_from_status(self):
        if 0 <= self.object.status <= len(EventDetailView.template_suffix_from_status):
            self.template_name_suffix = self.template_suffix_from_status[self.object.status]

    def get_context_0(self, context):
        proposals = DateProposal.objects.filter(user_event__event=self.object)
        event_votes = DateProposalVote.objects.filter(proposal__in=proposals)
        print(event_votes)
        my_votes = event_votes.filter(voting__user=self.request.user)
        print(my_votes)
        context['date_proposals'] = proposals
        context['my_votes'] = my_votes

    def get_context_status(self, context):
        context_status = [self.get_context_0]
        if 0 <= self.object.status <= len(context_status):
            context_status[self.object.status](context)

    def get_context_data(self, **kwargs):

        self.get_template_from_status()
        context = super().get_context_data(**kwargs)
        self.get_context_status(context)
        context['status_display'] = self.object.get_status_display()
        #
        return context

