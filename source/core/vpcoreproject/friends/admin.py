from django.contrib import admin

# Register your models here.
from friends.models import Friends, UserToFriends, JoinRequest

admin.site.register(Friends)
admin.site.register(UserToFriends)
admin.site.register(JoinRequest)
