from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory
from django.contrib import messages

from friends.models import Friends, UserToFriends
from places.models import Place
from users.models import MyUser
from events.forms_for_models import UserEventsRoleForm
from members.models import Member


class Event(models.Model):

    class EventStatus(models.IntegerChoices):
        DATE_SELECTION = 0, _('Date selection')
        PLACE_SELECTION = 1, _('Place selection')
        BOOKING = 2, _('Booking')
        CONFIRMED = 3, _('Confirmed')
        HISTORICAL = 4, _('Historical')

    name = models.CharField(max_length=30)
    friends = models.ForeignKey(Friends, on_delete=models.CASCADE)
    status = models.IntegerField(choices=EventStatus.choices, default=EventStatus.DATE_SELECTION)
    start = models.DateField(null=True)
    end = models.DateField(null=True)
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True)
    promoter = models.ForeignKey(UserToFriends, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}"

    @staticmethod
    def get_or_warning(id, request):
        try:
            return Event.objects.get(id=id)
        except ObjectDoesNotExist:
            messages.warning(request, f'Event with id {id} does not exist')
        return None

    @staticmethod
    def user_events(user: MyUser):
        return Event.objects.filter(usertoevent__user=user)

    @staticmethod
    def user_friends_events(user: MyUser):
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
        'form-TOTAL_FORMS': f'{count}',
        'form-INITIAL_FORMS': f'{count}',
        }
        form_id = 0
        for related_user in related_users:
            data.update(related_user.to_formset_data(form_id))
            form_id += 1

        formset_class = formset_factory(UserEventsRoleForm)
        formset = formset_class(data)
        return formset


class UserToEvent(Member):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} in {self.event.name}"

    @staticmethod
    def get_or_warning(user, event, request):
        try:
            return UserToEvent.objects.get(user=user, event=event)
        except ObjectDoesNotExist:
            messages.warning(request, f'User {user} does not belong to {event}')
        return None


class DateProposal(models.Model):
    user_event = models.ForeignKey(UserToEvent, on_delete=models.CASCADE)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return f"{self.start}-{self.end}"


class PlaceProposal(models.Model):
    user_event = models.ForeignKey(UserToEvent, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.place.name}"
