from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.forms import formset_factory
from django.utils.translation import gettext_lazy as _
from events.forms_for_models import UserEventsRoleForm
from friends.models import Friends
from members.models import Member
from places.models import Place
from users.models import FamilySize

UserModel = get_user_model()


class Event(models.Model):
    class EventStatus(models.IntegerChoices):
        DATE_SELECTION = 0, _("Date selection")
        PLACE_SELECTION = 1, _("Place selection")
        BOOKING = 2, _("Booking")
        CONFIRMED = 3, _("Confirmed")
        HISTORICAL = 4, _("Historical")

    name = models.CharField(max_length=30)
    friends = models.ForeignKey(Friends, on_delete=models.CASCADE)
    status = models.IntegerField(
        choices=EventStatus.choices, default=EventStatus.DATE_SELECTION
    )
    start = models.DateField(null=True)
    end = models.DateField(null=True)
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True)
    promoter = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}"

    @staticmethod
    def get_or_warning(id, request):
        try:
            return Event.objects.get(id=id)
        except ObjectDoesNotExist:
            messages.warning(request, f"Event with id {id} does not exist")
        return None

    @staticmethod
    def filter_by_user(user: UserModel):
        return Event.objects.filter(usertoevent__user=user)

    @staticmethod
    def user_friends_events(user: UserModel):
        return Event.objects.filter(friends__usertofriends__user=user)

    def test_user_role(self, user, role):
        try:
            relation = self.usertoevent_set.get(user=user)
        except ObjectDoesNotExist:
            return False
        return getattr(relation, role, False)

    def test_user(self, user):
        try:
            self.usertoevent_set.get(user=user)
        except ObjectDoesNotExist:
            return False
        return True

    def get_users_formset(self):
        related_users = self.usertoevent_set.all()
        count = related_users.count()
        data = {
            "form-TOTAL_FORMS": f"{count}",
            "form-INITIAL_FORMS": f"{count}",
        }
        form_id = 0
        for related_user in related_users:
            data.update(related_user.to_formset_data(form_id))
            form_id += 1

        formset_class = formset_factory(UserEventsRoleForm)
        formset = formset_class(data)
        return formset

    def get_participants_count(self):
        related_users = self.usertoevent_set.select_related("user").select_related(
            "user__default_family"
        )
        participants_count = FamilySize(adults=0, children=0, infants=0)

        for user_in_event in related_users:
            if user_in_event.user.default_family:
                participants_count += user_in_event.user.default_family
            else:
                participants_count.adults += 1

        return participants_count

    @staticmethod
    def get_status_text_by_val(value: int) -> str:
        choices = Event.EventStatus.choices
        found = list(filter(lambda choice: choice[0] == value, choices))
        if found:
            return found[0][1]
        return ""

    def go_back_1(self):
        self.status = 0
        self.start = None
        self.end = None
        self.save()

    def go_back_2(self):
        self.status = 1
        self.place = None
        self.promoter = None
        self.save()

    def go_back_3(self):
        self.status = 2
        self.save()

    def go_back(self):
        actions = [None, self.go_back_1, self.go_back_2, self.go_back_3]
        if 0 < self.status < len(actions):
            actions[self.status]()


class UserToEvent(Member):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} in {self.event.name}"

    @staticmethod
    def get_or_warning(user, event, request):
        try:
            return UserToEvent.objects.get(user=user, event=event)
        except ObjectDoesNotExist:
            messages.warning(request, f"User {user} does not belong to {event}")
        return None


class DateProposal(models.Model):
    user_event = models.ForeignKey(UserToEvent, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return f"{self.start} - {self.end}"

    @staticmethod
    def get_or_warning(id, request):
        try:
            return DateProposal.objects.get(id=id)
        except ObjectDoesNotExist:
            messages.warning(request, f"Date proposal with id {id} does not exist")
        return None


class DateProposalVote(models.Model):
    proposal = models.ForeignKey(DateProposal, on_delete=models.CASCADE)
    voting = models.ForeignKey(UserToEvent, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.proposal.start} - {self.proposal.end}"

    class Meta:
        unique_together = ("proposal", "voting")

    @staticmethod
    def get_or_warning(id, request):
        try:
            return DateProposalVote.objects.get(id=id)
        except ObjectDoesNotExist:
            messages.warning(request, f"Date proposal vote with id {id} does not exist")
        return None


class PlaceProposal(models.Model):
    user_event = models.ForeignKey(UserToEvent, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.place.name}"

    @staticmethod
    def get_or_warning(id, request):
        try:
            return PlaceProposal.objects.get(id=id)
        except ObjectDoesNotExist:
            messages.warning(request, f"Place proposal with id {id} does not exist")
        return None


class PlaceProposalVote(models.Model):
    proposal = models.ForeignKey(PlaceProposal, on_delete=models.CASCADE)
    voting = models.ForeignKey(UserToEvent, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.proposal.place}"

    class Meta:
        unique_together = ("proposal", "voting")

    @staticmethod
    def get_or_warning(id, request):
        try:
            return PlaceProposalVote.objects.get(id=id)
        except ObjectDoesNotExist:
            messages.warning(
                request, f"Place proposal vote with id {id} does not exist"
            )
        return None
