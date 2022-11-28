from django.contrib import admin

# Register your models here.
from places.models import Place, PlaceSize, Owner

admin.site.register(Place)
admin.site.register(PlaceSize)
admin.site.register(Owner)
