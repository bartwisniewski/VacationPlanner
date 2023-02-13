from django.urls import path
from chat.views import chat_box_standalone_view


urlpatterns = [
    path("<chat_id>/", chat_box_standalone_view, name="chat-standalone"),
]
