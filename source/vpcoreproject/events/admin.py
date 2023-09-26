from django.contrib import admin

# Register your models here.
from events.models import DateProposal, Event, PlaceProposal, UserToEvent

admin.site.register(Event)
admin.site.register(UserToEvent)
admin.site.register(DateProposal)
admin.site.register(PlaceProposal)
