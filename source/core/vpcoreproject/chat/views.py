from django.shortcuts import render


def chat_box_view(request, chat_box_name):
    # we will get the chatbox name from the url
    return render(request, "chat/chatbox.html", {"chat_box_name": chat_box_name})
