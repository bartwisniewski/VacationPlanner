from django.urls import path
from chat.views import chat_box_standalone_view


urlpatterns = [
    path("<str:chat_box_name>/", chat_box_standalone_view, name="chat-standalone"),
]
