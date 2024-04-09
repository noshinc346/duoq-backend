# from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Game, UserGame
from .serializers import GameSerializer, UserGameSerializer
from rest_framework import generics, filters
# from user_app.serializers import ProfileSerializer
from user_app.models import Profile
from user_app.serializers import ProfileSerializer
from django.contrib.auth.models import User


# Create your views here.

class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['game_name']
    ordering_fields = ['game_name']


# class UserGameList(generics.ListCreateAPIView):
#     serializer_class = UserGameSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['rank', 'game_id', 'status']
   
#     def get_queryset(self):
#         user_id = self.kwargs['user_id']
#         profile = self.get_profile(user_id)
#         return UserGame.objects.filter(profile_id=profile.id)
    
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['profile_serializer'] = ProfileSerializer(instance=self.get_profile(self.kwargs['user_id']))
#         return context

class UserGameList(generics.ListCreateAPIView):
    serializer_class = UserGameSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['rank', 'game_id', 'status']
   
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(pk=user_id)
        profile = user.profile  # Assuming you have a OneToOneField linking User to Profile
        return UserGame.objects.filter(profile_id=profile.id)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        user_id = self.kwargs['user_id']
        user = User.objects.get(pk=user_id)
        profile = user.profile  # Assuming you have a OneToOneField linking User to Profile
        context['profile_serializer'] = ProfileSerializer(instance=profile)
        return context

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GameSerializer
    lookup_field = 'id'

    def get_queryset(self):
        game_id = self.kwargs['id']
        return Game.objects.filter(id=game_id)

class UserGameDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserGameSerializer
    #lookup_field = 'id'

    def get_queryset(self):
        profile_id = self.kwargs['profile_id']
        game_id = self.kwargs['game_id']
        return UserGame.objects.filter(profile_id=profile_id).filter(game_id=game_id)
