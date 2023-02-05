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
        if not hasattr(self, "object"):
            return None
        chat_parent = self.object
        chat_object = self.chat_model.get_or_warning(chat_parent, request)
        return chat_object.chat

    def messages_as_string(self):
        pass

    def get_chats(self, request):
        possible_parents = self.model.filter_by_user(request.user)
        related_chats_list = self.chat_model.filter_by_parent_object(possible_parents)
        if not related_chats_list:
            return None
        chat_list = [chat.chat for chat in related_chats_list]
        return chat_list

    def add_chat_context(self, context, request):
        self.chat_model = self.get_chat_model()
        if not self.chat_model:
            return
        chat = self.get_chat(request)
        if chat:
            chat_context = {
                "chat_id": chat.id,
                "chat_messages": chat.last_x_messages_as_text(20),
            }
            context.update(chat_context)
            return

        chat_list = self.get_chats(request)
        if chat_list:
            chat_context = {
                "chats": chat_list,
            }
            context.update(chat_context)
