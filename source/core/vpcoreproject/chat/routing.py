from chat import consumers
from django.urls import re_path


websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<chat_id>\w+)/$", consumers.ChatRoomConsumer.as_asgi()),
]
