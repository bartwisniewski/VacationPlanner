from django.contrib import admin

# Register your models here.
from users.models import FamilySize, MyUser

admin.site.register(MyUser)
admin.site.register(FamilySize)
