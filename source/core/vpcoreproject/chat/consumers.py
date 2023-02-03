import json
from django.contrib.auth import get_user_model

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Chat, Message


UserModel = get_user_model()


class ChatRoomConsumer(AsyncWebsocketConsumer):
    group_name_prefix = "chat_"

    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.group_name = f"{ChatRoomConsumer.group_name_prefix}{self.chat_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        await self.save_message(message, username)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chatbox_message",
                "message": message,
                "username": username,
            },
        )

    @database_sync_to_async
    def save_message(self, message, username):
        chat_id = self.get_id_from_name()
        chat = Chat.get_or_none(chat_id)
        sender = UserModel.get_by_name_or_none(username)
        if chat and sender:
            Message.objects.create(chat=chat, sender=sender, message=message)

    def get_id_from_name(self):
        prefix_len = len(ChatRoomConsumer.group_name_prefix)
        chat_id = self.group_name[prefix_len:]
        return chat_id

    async def chatbox_message(self, event):
        message = event["message"]
        username = event["username"]

        send_message = f"{username}: {message}"

        await self.send(
            text_data=json.dumps(
                {
                    "message": send_message,
                    "username": username,
                }
            )
        )

    pass
