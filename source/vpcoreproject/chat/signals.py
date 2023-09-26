from chat.models import Chat, EventChat, FriendsChat
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from events.models import Event
from friends.models import Friends


@receiver(post_save, sender=Event)
def create_chat_event(sender, instance, created, **kwargs):
    if created:
        new_chat = Chat.objects.create()
        EventChat.objects.create(event=instance, chat=new_chat)


@receiver(post_save, sender=Friends)
def create_chat_friends(sender, instance, created, **kwargs):
    if created:
        new_chat = Chat.objects.create()
        FriendsChat.objects.create(friends=instance, chat=new_chat)


@receiver(post_delete, sender=EventChat)
def delete_chat_event(sender, instance, *args, **kwargs):
    chat = instance.chat
    chat.delete()


@receiver(post_delete, sender=FriendsChat)
def delete_chat_friends(sender, instance, *args, **kwargs):
    chat = instance.chat
    chat.delete()
