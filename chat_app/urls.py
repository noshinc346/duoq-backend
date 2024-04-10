from django.urls import path
from .views import ChatList

urlpatterns = [
        path('chat/', ChatList.as_view(), name='chat-list'),
        ]

