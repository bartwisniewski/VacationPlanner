from django.db import models
from users.models import MyUser

# Create your models here.


class Friends(models.Model):
    nickname = models.CharField(max_length=30)

    def __str__(self):
        return self.nickname


class UserToFriends(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    friends = models.ForeignKey(Friends, on_delete=models.CASCADE)
    admin = models.BooleanField(default=False)
    owner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} is in {self.friends.nickname}"


class JoinRequest(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    friends = models.ForeignKey(Friends, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} request joining {self.friends.nickname}"
