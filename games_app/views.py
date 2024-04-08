from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.response import Response
from .models import Game, UserGame, Profile
from .serializers import GameSerializer, UserGameSerializer, UserSerializer, ProfileSerializer
from rest_framework import generics, filters
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from rest_framework import generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['game_name']
    ordering_fields = ['game_name']


class UserGameList(generics.ListCreateAPIView):
    serializer_class = UserGameSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['rank', 'game_id', 'status']
   
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        profile_id = Profile.object.filter(user_id = user_id)[id]
        return UserGame.object.filter(profile_id=profile_id)


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GameSerializer
    lookup_field = 'id'

    def get_queryset(self):
        game_id = self.kwargs['id']
        return Game.objects.filter(id=game_id)

class UserGameDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserGameSerializer
   # lookup_field = 'id'

    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        game_id = self.kwargs['game_id']
        return UserGame.objects.filter(profile_id=profile_id, game_id=game_id)


@login_required
def profile(request):
    return render(request, 'users/profile')

class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })

# User Login
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })
  
  
  #Profile View
class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
   # lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
      user = self.request.user
      return Profile.objects.filter(user=user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj
