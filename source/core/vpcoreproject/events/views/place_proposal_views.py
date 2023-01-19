import re

from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View, TemplateView
from django.views.generic.edit import CreateView, DeleteView

from events.models import PlaceProposal, PlaceProposalVote, Event, UserToEvent
from events.forms import PlaceProposalForm
from places.models import Place
from events.views.date_proposal_views import (
    ProposalVoteView,
    ProposalUnvoteView,
    ProposalAcceptView,
)
from events.helpers import compile_filter


class PlaceProposalCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = PlaceProposal
    form_class = PlaceProposalForm
    permission_denied_message = f"you are not participant of this event"
    phrase_min_length = 3

    def get_success_url(self):
        event = self.get_event(self.request)
        if event:
            return reverse("event-detail", kwargs={"pk": event.id})
        return reverse("event-list")

    def test_func(self):
        event = self.get_event(self.request)
        return event.test_user(self.request.user)

    def handle_no_permission(self):
        messages.warning(self.request, self.permission_denied_message)
        return HttpResponseRedirect(self.get_success_url())

    def get_event(self, request):
        event_id = self.kwargs["pk"]
        return Event.get_or_warning(event_id, request)

    def get_context_data(self, **kwargs):
        event = self.get_event(self.request)
        context = super().get_context_data(**kwargs)
        filter_phrase = self.request.GET.get("q", "")
        if event:
            context["event"] = event
            context["participants_count"] = event.get_participants_count()
        if len(filter_phrase) >= self.phrase_min_length:
            context["filter_phrase"] = filter_phrase
        return context

    def get_queryset(self):
        filter_phrase = self.request.GET.get("q", "")
        event = self.get_event(self.request)
        proposals = PlaceProposal.objects.filter(user_event__event=event)
        queryset = Place.objects.filter(created_by=self.request.user).exclude(
            placeproposal__in=proposals
        )
        participants = event.get_participants_count()
        queryset = Place.add_filter_by_capacity(queryset, participants)
        phrases = re.split(",\s*", filter_phrase)

        for phrase in phrases:
            if len(phrase) >= self.phrase_min_length:
                compiled_filter = Place.compile_filter(phrase)
                queryset = queryset.filter(compiled_filter)
        return queryset

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields["place"].queryset = self.get_queryset()
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


class PlaceProposalCreateViewAddFilter(View):
    def post(self, request, *args, **kwargs):
        event_id = kwargs["pk"]
        place_proposal_create_url = reverse(
            "event-place-propose", kwargs={"pk": event_id}
        )
        q = self.request.POST.get("filter_phrase", "")
        if q:
            place_proposal_create_url += f"?q={q}"
        return HttpResponseRedirect(place_proposal_create_url)


class PlaceProposalDeleteView(UserPassesTestMixin, DeleteView):
    model = PlaceProposal
    template_name = "events/proposal_confirm_delete.html"
    permission_denied_message = f"you can only delete your own proposal"

    def get_success_url(self):
        event = self.get_object().user_event.event
        if event:
            return reverse("event-detail", kwargs={"pk": event.id})
        return reverse("event-list")

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

    @staticmethod
    def send_mail_to_promoter(promoter):
        send_mail(
            "Your proposal was selected",
            "Congratulations, your place proposal has been chosen by the group. "
            "Now you need to process with booking and confirm it in the vacation planner",
            settings.EMAIL_HOST_USER,
            [promoter.email],
            fail_silently=True,
        )

    def post_action(self):
        event = self.object.user_event.event
        promoter = self.object.user_event.user

        event.place = self.object.place
        event.status = Event.EventStatus.BOOKING
        event.promoter = promoter
        event.save()
        self.send_mail_to_promoter(promoter)
