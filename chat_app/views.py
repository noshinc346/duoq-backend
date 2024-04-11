from django.shortcuts import render
from rest_framework import generics, permissions, filters
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import ChatSerializer, MessageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import Chat, Message
from user_app.models import Profile
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
@login_required
def profile(request):
    return render(request, 'users/profile')


class ChatList(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user1', 'user2']
    
    def get_queryset(self):
        user = self.request.user
        profile = Profile.objects.filter(user=user)
        return Chat.objects.filter(Q(user1=profile[0]) | Q(user2=profile[0]))


class MessageList(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['time']

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat = chat_id)


class ChatDetail(generics.RetrieveDestroyAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        other_id = self.kwargs['other_id']
        user = self.request.user
        profile = Profile.objects.filter(user=user)
        return Chat.objects.filter(Q(user1=profile[0]) | Q(user2=profile[0])).filter(Q(user1=other_id) | Q(user2=other_id))

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj

