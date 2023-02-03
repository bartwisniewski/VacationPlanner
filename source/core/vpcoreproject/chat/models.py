from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from events.models import Event
from friends.models import Friends

UserModel = get_user_model()


class Chat(models.Model):
    @staticmethod
    def get_or_none(chat_id):
        try:
            return Chat.objects.get(id=chat_id)
        except ObjectDoesNotExist:
            pass
        return None

    def last_x_messages(self, x):
        return self.message_set.order_by("-updated").all()[:x]

    def last_x_messages_as_text(self, x):
        messages_strings = [
            message.str_for_chat() for message in self.last_x_messages(x)
        ]
        printout = "\n".join(messages_strings) + "\n"
        return printout


class Message(models.Model):
    name = models.CharField(max_length=30)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.updated.strftime('%Y-%m-%d %H:%M')} | {self.sender}\n{self.message}"
        )

    def str_for_chat(self):
        return f"{self.sender}:{self.message}"


class EventChat(models.Model):
    chat = models.OneToOneField(Chat, on_delete=models.CASCADE)
    event = models.OneToOneField(Event, on_delete=models.CASCADE)

    @staticmethod
    def get_or_warning(owner, request):
        try:
            return EventChat.objects.get(event=owner)
        except ObjectDoesNotExist:
            messages.warning(request, f"EventChat of Event {owner} does not exist")
        return None


class FriendsChat(models.Model):
    chat = models.OneToOneField(Chat, on_delete=models.CASCADE)
    friends = models.OneToOneField(Friends, on_delete=models.CASCADE)

    @staticmethod
    def get_or_warning(owner, request):
        try:
            return FriendsChat.objects.get(friends=owner)
        except ObjectDoesNotExist:
            messages.warning(
                request, f"FriendsChat of Friends group {owner} does not exist"
            )
        return None
