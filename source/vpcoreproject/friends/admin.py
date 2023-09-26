from django.contrib import admin

# Register your models here.
from friends.models import Friends, JoinRequest, UserToFriends

admin.site.register(Friends)
admin.site.register(UserToFriends)
admin.site.register(JoinRequest)
