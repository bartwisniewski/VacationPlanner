from django.contrib import admin

# Register your models here.
from users.models import MyUser, FamilySize

admin.site.register(MyUser)
admin.site.register(FamilySize)
