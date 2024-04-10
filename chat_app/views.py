from django.shortcuts import render
from rest_framework import generics, permissions
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
    
    def get_queryset(self):
        user = self.request.user
        profile = Profile.objects.filter(user=user)
        return Chat.objects.filter(Q(user1=profile[0]) | Q(user2=profile[0]))
