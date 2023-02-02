from django.shortcuts import render
from chat.models import EventChat, FriendsChat, Message


def chat_box_standalone_view(request, chat_id):
    # we will get the chatbox name from the url
    return render(request, "chat/chatbox_standalone.html", {"chat_id": chat_id})


class ChatMixin:
    chat_models = {"Event": EventChat, "Friends": FriendsChat}

    def get_chat_model(self):
        if not self.model:
            return None
        return ChatMixin.chat_models.get(self.model.__name__)

    def get_chat(self, request):
        if not self.object:
            return None
        owner = self.object
        chat_model = self.get_chat_model()
        chat_object = chat_model.get_or_warning(owner, request)
        return chat_object.chat

    def messages_as_string(self):
        pass

    def add_chat_context(self, context, request):
        chat = self.get_chat(request)
        chat_context = {
            "chat_id": chat.id,
            "chat_messages": chat.last_x_messages_as_text(20),
        }
        context.update(chat_context)
