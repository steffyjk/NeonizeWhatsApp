from django.shortcuts import render, get_object_or_404
from .models import Chat, Message

def chat_list(request):
    chats = Chat.objects.all()
    return render(request, 'chat/chat_list.html', {'chats': chats})

def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, chat_id=chat_id)
    messages = Message.objects.filter(chat=chat).order_by('timestamp')
    return render(request, 'chat/chat_detail.html', {'chat': chat, 'messages': messages})

