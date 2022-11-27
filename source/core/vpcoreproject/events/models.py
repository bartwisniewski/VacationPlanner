from django.db import models
from django.utils.translation import gettext_lazy as _

from friends.models import Friends
from places.models import Place
from users.models import MyUser


class Event(models.Model):

    class EventStatus(models.IntegerChoices):
        DATE_SELECTION = 0, _('Date selection')
        PLACE_SELECTION = 1, _('Place selection')
        BOOKING = 2, _('Booking')
        CONFIRMED = 3, _('Confirmed')
        HISTORICAL = 4, _('Historical')

    friends = models.ForeignKey(Friends, on_delete=models.CASCADE)
    status = models.IntegerField(choices=EventStatus.choices)
    start = models.DateField()
    end = models.DateField()
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True)
    promoter = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)

