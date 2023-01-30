from django.shortcuts import render
from chat.models import EventChat, FriendsChat


def chat_box_standalone_view(request, chat_box_name):
    # we will get the chatbox name from the url
    return render(
        request, "chat/chatbox_standalone.html", {"chat_box_name": chat_box_name}
    )


class ChatMixin:
    chat_models = {"Event": EventChat, "Friends": FriendsChat}

    def get_chat_model(self):
        if not self.model:
            return None
        return ChatMixin.chat_models.get(self.model.__name__)

    def get_chat_id(self, request):
        if not self.object:
            return None
        owner = self.object
        chat_model = self.get_chat_model()
        chat_object = chat_model.get_or_warning(owner, request)
        return chat_object.chat.id

    def add_chat_context(self, context, request):
        chat_context = {"chat_name": self.get_chat_id(request)}
        context.update(chat_context)
