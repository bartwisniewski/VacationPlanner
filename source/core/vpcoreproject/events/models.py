from django.db import models
from django.utils.translation import gettext_lazy as _

from friends.models import Friends, UserToFriends
from places.models import Place
from users.models import MyUser

class Event(models.Model):

    class EventStatus(models.IntegerChoices):
        DATE_SELECTION = 0, _('Date selection')
        PLACE_SELECTION = 1, _('Place selection')
        BOOKING = 2, _('Booking')
        CONFIRMED = 3, _('Confirmed')
        HISTORICAL = 4, _('Historical')

    name = models.CharField(max_length=30)
    friends = models.ForeignKey(Friends, on_delete=models.CASCADE)
    status = models.IntegerField(choices=EventStatus.choices)
    start = models.DateField()
    end = models.DateField()
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True)
    promoter = models.ForeignKey(UserToFriends, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}"


class UserToEvent(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    admin = models.BooleanField(default=False)
    owner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} in {self.event.nickname}"


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
