from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Count, Case, Value, BooleanField, When

from events.models import Event, UserToEvent, DateProposal, DateProposalVote, PlaceProposal, PlaceProposalVote


class EventDetailView(UserPassesTestMixin, DetailView):
    model = Event
    template_suffix_from_status = ["_detail_0", "_detail_1", "_detail_2"]
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

    def set_template_name_suffix(self):
        if 0 <= self.object.status <= len(EventDetailView.template_suffix_from_status):
            self.template_name_suffix = self.template_suffix_from_status[self.object.status]

    def get_votes(self, context, proposals, vote_model):
        event_votes = vote_model.objects.filter(proposal__in=proposals)
        my_votes = event_votes.filter(voting__user=self.request.user)
        return my_votes

    def annotate_i_voted(self, proposals, lookup_vote_model):
        # my_voted = proposals.filter(dateproposalvote__voting__user=self.request.user)
        lookup = f"{lookup_vote_model}__voting__user"
        my_voted = proposals.filter(**{lookup: self.request.user})
        return proposals.annotate(
            i_voted=Case(
                When(id__in=my_voted, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )

    def get_proposals(self, context, lookup_vote_model, proposal_model):
        proposals = proposal_model.objects.filter(user_event__event=self.object).annotate(Count(lookup_vote_model)) \
            .order_by(f'-{lookup_vote_model}__count')
        proposals = self.annotate_i_voted(proposals=proposals, lookup_vote_model=lookup_vote_model)
        return proposals

    def get_context_0(self, context):
        proposals = self.get_proposals(context=context, lookup_vote_model='dateproposalvote',
                                       proposal_model=DateProposal)
        my_votes = self.get_votes(context=context, vote_model=DateProposalVote, proposals=proposals)
        context['my_votes'] = my_votes
        context['proposals'] = proposals

    def get_context_1(self, context):
        proposals = self.get_proposals(context=context, lookup_vote_model='placeproposalvote',
                                       proposal_model=PlaceProposal)
        my_votes = self.get_votes(context=context, vote_model=PlaceProposalVote, proposals=proposals)
        context['my_votes'] = my_votes
        context['proposals'] = proposals

    def get_context_status(self, context):
        context_status = [self.get_context_0, self.get_context_1]
        if 0 <= self.object.status < len(context_status):
            context_status[self.object.status](context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.get_context_status(context)
        context['status_display'] = self.object.get_status_display()
        #
        return context

    def get(self, request, *args, **kwargs):
        self.set_template_name_suffix()
        return super().get(request, *args, **kwargs)
