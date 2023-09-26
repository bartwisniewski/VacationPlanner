from django.contrib import admin

# Register your models here.
from places.models import Owner, Place, PlaceSize

admin.site.register(Place)
admin.site.register(PlaceSize)
admin.site.register(Owner)
