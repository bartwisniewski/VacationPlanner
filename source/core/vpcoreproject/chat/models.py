from django.db import models
from django.contrib.auth import get_user_model

from events.models import Event
from friends.models import Friends

UserModel = get_user_model()


class Chat(models.Model):
    pass


class Message(models.Model):
    name = models.CharField(max_length=30)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class EventChat(models.Model):
    chat = models.OneToOneField(Chat, on_delete=models.CASCADE)
    event = models.OneToOneField(Event, on_delete=models.CASCADE)


class FriendsChat(models.Model):
    chat = models.OneToOneField(Chat, on_delete=models.CASCADE)
    friends = models.OneToOneField(Friends, on_delete=models.CASCADE)
