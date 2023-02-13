from chat import consumers
from django.urls import path


websocket_urlpatterns = [
    path(r"ws/chat/<chat_id>/", consumers.ChatRoomConsumer.as_asgi()),
]
