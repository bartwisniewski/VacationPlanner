from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View, TemplateView
from django.views.generic.edit import CreateView, DeleteView


from events.models import DateProposal, DateProposalVote, Event, UserToEvent
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


class DateProposalVoteView(LoginRequiredMixin, View):

    def __init__(self, *args, **kwargs):
        self.object = None
        super().__init__(*args, **kwargs)

    def get_object(self):
        date_proposal_id = self.kwargs['pk']
        date_proposal = DateProposal.get_or_warning(date_proposal_id, self.request)
        self.object = date_proposal

    def get_target_url(self):
        if self.object:
            event = self.object.user_event.event
            return reverse('event-detail', kwargs={'pk': event.id})
        return reverse('event-list')

    def post(self, request, *args, **kwargs):
        self.get_object()
        target_url = self.get_target_url()

        if not self.object:
            return HttpResponseRedirect(target_url)

        user = request.user
        event = self.object.user_event.event
        user_to_event = UserToEvent.get_or_warning(user, event, request)

        if not user_to_event:
            return HttpResponseRedirect(target_url)

        proposal = self.object
        date_proposal_vote, created = DateProposalVote.objects.get_or_create(proposal=proposal, voting=user_to_event)
        if created:
            messages.info(self.request, f'You have successfully voted on: {proposal}')
        else:
            messages.warning(self.request, f'You have already voted on: {proposal}')

        return HttpResponseRedirect(target_url)


class DateProposalUnvoteView(LoginRequiredMixin, View):

    def __init__(self, *args, **kwargs):
        self.object = None
        super().__init__(*args, **kwargs)

    def get_object(self):
        date_proposal_vote_id = self.kwargs['pk']
        date_proposal_vote = DateProposalVote.get_or_warning(date_proposal_vote_id, self.request)
        self.object = date_proposal_vote

    def get_target_url(self):
        if self.object:
            event = self.object.proposal.user_event.event
            return reverse('event-detail', kwargs={'pk': event.id})
        return reverse('event-list')

    def test_func(self, request):
        return request.user == self.object.voting.user

    def post(self, request, *args, **kwargs):
        self.get_object()
        target_url = self.get_target_url()

        if not self.object:
            return HttpResponseRedirect(target_url)

        if not self.test_func(request):
            messages.warning(request, f'You can only unvote your own votes')
            return HttpResponseRedirect(target_url)

        proposal_string = str(self.object)
        self.object.delete()
        messages.info(request, f'You have successfully unvoted: {proposal_string}')
        return HttpResponseRedirect(target_url)


class DateProposalAcceptView(UserPassesTestMixin, TemplateView):
    template_name = "events/date_proposal_accept_confirm.html"
    permission_role = 'admin'
    permission_denied_message = f'you are not {permission_role} of this event'

    def __init__(self, *args, **kwargs):
        self.object = None
        super().__init__(*args, **kwargs)

    def get_object(self):
        date_proposal_id = self.kwargs['pk']
        date_proposal = DateProposal.get_or_warning(date_proposal_id, self.request)
        self.object = date_proposal

    def get_target_url(self):
        if self.object:
            event = self.object.user_event.event
            return reverse('event-detail', kwargs={'pk': event.id})
        return reverse('event-list')

    def test_func(self):
        self.get_object()
        event = self.object.user_event.event
        return event.test_user_role(self.request.user, DateProposalAcceptView.permission_role)

    def handle_no_permission(self):
        messages.warning(self.request, self.permission_denied_message)
        return HttpResponseRedirect(self.get_target_url())

    def get(self, request, *args, **kwargs):
        self.get_object()
        if self.object:
            context = self.get_context_data(**kwargs)
            context['date_proposal'] = self.object
            return self.render_to_response(context)

        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        self.get_object()
        target_url = self.get_target_url()
        if not self.object:
            return HttpResponseRedirect(target_url)

        event = self.object.user_event.event
        event.start = self.object.start
        event.end = self.object.end
        event.status = Event.EventStatus.PLACE_SELECTION
        event.save()

        return HttpResponseRedirect(target_url)
