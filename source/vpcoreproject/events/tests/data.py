from events.models import Event, UserToEvent
from friends.tests.data import friends
from users.tests.data import users

# class EventStatus(models.IntegerChoices):
#     DATE_SELECTION = 0, _("Date selection")
#     PLACE_SELECTION = 1, _("Place selection")
#     BOOKING = 2, _("Booking")
#     CONFIRMED = 3, _("Confirmed")
#     HISTORICAL = 4, _("Historical")
#
#
# name = models.CharField(max_length=30)
# friends = models.ForeignKey(Friends, on_delete=models.CASCADE)
# status = models.IntegerField(
#     choices=EventStatus.choices, default=EventStatus.DATE_SELECTION
# )
# start = models.DateField(null=True)
# end = models.DateField(null=True)
# place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True)
# promoter = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)


def generate():
    events = [
        Event.objects.get_or_create(name="event1", friends=friends[0], status=0),
        Event.objects.get_or_create(
            name="event2",
            friends=friends[0],
            status=1,
            start="2023-06-01",
            end="2023-06-08",
        ),
        Event.objects.get_or_create(
            name="event3",
            friends=friends[1],
            status=2,
            start="2023-06-01",
            end="2023-06-08",
        ),
    ]
    user_to_event = [
        UserToEvent.objects.get_or_create(
            event=events[0], user=users[0], admin=True, owner=True
        ),
        UserToEvent.objects.get_or_create(
            event=events[0], user=users[1], admin=False, owner=False
        ),
        UserToEvent.objects.get_or_create(
            event=events[1], user=users[1], admin=True, owner=True
        ),
    ]
    return events, user_to_event


events, user_to_event = generate()
