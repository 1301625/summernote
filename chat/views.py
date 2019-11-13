from django.shortcuts import render

from .models import Chatroom

def room(request, pk):
    chat_message = Chatroom.objects.filter(post_id=pk)
    content = {
        'chat_message' : chat_message,
        'pk' : pk
    }
    return render(request, '', content)


