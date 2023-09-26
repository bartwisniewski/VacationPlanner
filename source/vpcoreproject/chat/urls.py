from chat.views import chat_box_standalone_view
from django.urls import path

urlpatterns = [
    path("<chat_id>/", chat_box_standalone_view, name="chat-standalone"),
]
