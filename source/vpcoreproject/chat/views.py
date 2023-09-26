from chat.models import Chat, EventChat, FriendsChat
from django.shortcuts import render


def chat_box_standalone_view(request, chat_id):
    # we will get the chatbox name from the url
    return render(request, "chat/chatbox_standalone.html", {"chat_id": chat_id})


class ChatDataGenerator:
    def __init__(self, view):
        self.view = view

    def add_chat_context(self, context, request) -> None:
        self.update_chat_list_data(self.get_chats(request), context)
        self.update_chat_data(self.get_chat(request), context)

    @staticmethod
    def test(view) -> bool:
        raise NotImplementedError

    def get_chats(self, request):
        raise NotImplementedError

    def get_chat(self, request):
        raise NotImplementedError

    @staticmethod
    def update_chat_data(chat, context):
        if chat:
            chat_context = {
                "chat_id": chat.id,
                "chat_parent": chat.parent_object,
                "chat_messages": chat.last_x_messages_as_text(20),
            }
            context.update(chat_context)

    @staticmethod
    def update_chat_list_data(chat_list, context) -> None:
        if chat_list:
            chat_context = {
                "list": True,
                "chats": chat_list,
            }
            context.update(chat_context)


class UserChatData(ChatDataGenerator):
    @staticmethod
    def test(view) -> bool:
        return True

    def get_chats(self, request):
        chats = Chat.filter_by_user(request.user)
        if not chats:
            return None
        return [{"chat": chat, "parent": chat.parent_object} for chat in chats]

    def get_chat(self, request):
        if request.GET.get("chat"):
            return Chat.get_or_none(request.GET.get("chat"))
        return None


class ObjectListChatData(ChatDataGenerator):
    @staticmethod
    def test(view) -> bool:
        return view.chat_model is not None

    def get_chats(self, request):
        possible_parents = self.view.model.filter_by_user(request.user)
        related_chats_list = self.view.chat_model.filter_by_parent_object(
            possible_parents
        )
        if not related_chats_list:
            return None
        chat_list = [
            {"chat": chat.chat, "parent": chat.parent_object}
            for chat in related_chats_list
        ]
        return chat_list

    def get_chat(self, request):
        if request.GET.get("chat"):
            return Chat.get_or_none(request.GET.get("chat"))
        return None


class SingleObjectChatData(ChatDataGenerator):
    @staticmethod
    def test(view) -> bool:
        return view.chat_model is not None and hasattr(view, "object")

    def get_chats(self, request):
        return None

    def get_chat(self, request):
        chat_parent = self.view.object
        chat_object = self.view.chat_model.get_or_create(chat_parent)
        return chat_object.chat


class ChatMixin:
    CHAT_MODELS = {"Event": EventChat, "Friends": FriendsChat}
    GENERATORS = [SingleObjectChatData, ObjectListChatData, UserChatData]

    def __init__(self):
        self.model = None
        self.chat_model = None

    def get_chat_model(self):
        if not hasattr(self, "model") or not self.model:
            return None
        return ChatMixin.CHAT_MODELS.get(self.model.__name__)

    def messages_as_string(self):
        pass

    def chat_generator(self) -> ChatDataGenerator:
        for generator in ChatMixin.GENERATORS:
            if generator.test(self):
                return generator(view=self)
        return None

    def add_chat_context(self, context, request):
        self.chat_model = self.get_chat_model()
        chat_generator = self.chat_generator()
        if chat_generator:
            chat_generator.add_chat_context(context, request)
