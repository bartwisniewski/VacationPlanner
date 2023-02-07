from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from events.models import Event
from friends.models import Friends

UserModel = get_user_model()


class Chat(models.Model):
    related_chats = ["eventchat", "friendschat"]

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

    def get_parent_object(self):
        for related_chat_name in self.related_chats:
            try:
                related_chat_object = getattr(self, related_chat_name)
                return related_chat_object.parent_object
            except getattr(Chat, related_chat_name).RelatedObjectDoesNotExist:
                print("does not exist")
        return None

    parent_object = property(get_parent_object)


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

    @staticmethod
    def message_format_for_chat(username: str, message: str) -> str:
        return f"{username}:{message}"

    def str_for_chat(self):
        return Message.message_format_for_chat(str(self.sender), str(self.message))


class EventChat(models.Model):
    chat = models.OneToOneField(Chat, on_delete=models.CASCADE)
    event = models.OneToOneField(Event, on_delete=models.CASCADE)

    @staticmethod
    def get_or_warning(parent_object, request):
        try:
            return EventChat.objects.get(event=parent_object)
        except ObjectDoesNotExist:
            messages.warning(
                request, f"EventChat of Event {parent_object} does not exist"
            )
        return None

    @staticmethod
    def filter_by_parent_object(parent_object_list):
        return EventChat.objects.filter(event__in=parent_object_list)

    def get_parent_object(self):
        return self.event

    parent_object = property(get_parent_object)


class FriendsChat(models.Model):
    chat = models.OneToOneField(Chat, on_delete=models.CASCADE)
    friends = models.OneToOneField(Friends, on_delete=models.CASCADE)

    @staticmethod
    def get_or_warning(parent_object, request):
        try:
            return FriendsChat.objects.get(friends=parent_object)
        except ObjectDoesNotExist:
            messages.warning(
                request, f"FriendsChat of Friends group {parent_object} does not exist"
            )
        return None

    @staticmethod
    def filter_by_parent_object(parent_object_list):
        return FriendsChat.objects.filter(friends__in=parent_object_list)

    def get_parent_object(self):
        return self.friends

    parent_object = property(get_parent_object)
