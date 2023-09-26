from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from events.helpers import UserToEventUpdateManager
from events.models import Event, PlaceProposal, UserToEvent
from friends.models import Friends
from members.helpers import SingleObjectUserRoleRequiredView, owner_only


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = [
        "name",
        "friends",
    ]
    success_url = reverse_lazy("events-list")

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields["friends"].queryset = Friends.objects.filter(
            usertofriends__user=self.request.user
        )
        return form

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        UserToEvent(
            user=self.request.user, event=self.object, admin=True, owner=True
        ).save()
        return HttpResponseRedirect(self.get_success_url())


class EventUpdateView(SingleObjectUserRoleRequiredView, UpdateView):
    model = Event
    fields = ("name",)
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("events-list")
    permission_role = "admin"
    permission_denied_message = "you are not admin of this event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        related_users = self.object.usertoevent_set.all()
        context["users"] = related_users
        formset = self.object.get_users_formset()
        context["users_formset"] = formset
        return context

    @owner_only
    def update_members(self, request, *args, **kwargs):
        count = int(request.POST.get("form-TOTAL_FORMS", 0))
        post_data = request.POST
        UserToEventUpdateManager.update_members(count, post_data)

    def members_changed(self, request, *args, **kwargs):
        count = int(request.POST.get("form-TOTAL_FORMS", 0))
        post_data = request.POST
        return UserToEventUpdateManager.members_changed(count, post_data)

    def post(self, request, *args, **kwargs):
        if self.members_changed(request, *args, **kwargs):
            self.update_members(request, *args, **kwargs)
        return super().post(request, *args, **kwargs)


class EventDeleteView(SingleObjectUserRoleRequiredView, DeleteView):
    model = Event
    success_url = reverse_lazy("events-list")
    permission_role = "owner"
    permission_denied_message = f"you are not {permission_role} of this event"


class UserToEventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserToEvent
    permission_denied_message = "you are not permited to delete this member"
    success_url = reverse_lazy("events-list")

    def test_func(self):
        self.object = self.get_object()
        event = self.object.event
        deleted_is_admin = self.object.admin
        deleted_is_owner = self.object.owner
        user_is_admin = event.test_user_role(self.request.user, "admin")
        user_is_owner = event.test_user_role(self.request.user, "owner")

        return (user_is_admin and not deleted_is_admin) or (
            user_is_owner and not deleted_is_owner
        )

    def handle_no_permission(self):
        messages.warning(self.request, self.permission_denied_message)
        return HttpResponseRedirect(self.get_success_url())


class EventStateBackView(UserPassesTestMixin, TemplateView):
    model = Event
    template_name = "events/state_back_confirm.html"
    permission_role = "admin"
    permission_denied_message = f"you are not {permission_role} of this event"

    def __init__(self, *args, **kwargs):
        self.object = None
        super().__init__(*args, **kwargs)

    def get_object(self):
        object_id = self.kwargs["pk"]
        object_instance = self.model.get_or_warning(object_id, self.request)
        self.object = object_instance

    def get_target_url(self):
        if self.object:
            event = self.object
            return reverse("event-detail", kwargs={"pk": event.id})
        return reverse("event-list")

    def is_promoter(self):
        event = self.object
        if event.status in [Event.EventStatus.BOOKING, Event.EventStatus.CONFIRMED]:
            return self.request.user == event.promoter
        return False

    def test_func(self):
        self.get_object()
        event = self.object
        is_admin = event.test_user_role(self.request.user, self.permission_role)
        return self.is_promoter() or is_admin

    def handle_no_permission(self):
        messages.warning(self.request, self.permission_denied_message)
        return HttpResponseRedirect(self.get_target_url())

    def get(self, request, *args, **kwargs):
        self.get_object()
        if self.object and self.object.status > 0:
            context = self.get_context_data(**kwargs)
            context["object"] = self.object
            context["previous_step"] = Event.get_status_text_by_val(
                self.object.status - 1
            )

            return self.render_to_response(context)
        target_url = self.get_target_url()
        return HttpResponseRedirect(target_url)

    def post_action(self):
        if self.object.status == Event.EventStatus.BOOKING and self.is_promoter():
            place_proposal = PlaceProposal.objects.get(
                place=self.object.place, user_event__event=self.object
            )
            place_proposal.delete()
        self.object.go_back()

    def post(self, request, *args, **kwargs):
        self.get_object()
        target_url = self.get_target_url()
        if not self.object:
            return HttpResponseRedirect(target_url)

        self.post_action()

        return HttpResponseRedirect(target_url)
