from django.urls import path
from .views import ChatList, MessageList, ChatDetail

urlpatterns = [
        path('', ChatList.as_view(), name='chat-list'),
        path('messages/<int:chat_id>/', MessageList.as_view(), name='message-list'),
        path('<int:other_id>/', ChatDetail.as_view(), name='chat-detail'),
        ]

