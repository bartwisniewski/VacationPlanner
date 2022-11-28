from django.contrib import admin

# Register your models here.
from events.models import Event, UserToEvent, DateProposal, PlaceProposal

admin.site.register(Event)
admin.site.register(UserToEvent)
admin.site.register(DateProposal)
admin.site.register(PlaceProposal)
