from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Game, UserGame
from .serializers import GameSerializer, UserGameSerializer
from rest_framework import generics, filters
from user_app.models import Profile


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
    search_fields = ['rank']
   
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        profile_id = Profile.object.filter(user_id = user_id)[id]
        return UserGame.object.filter(profile_id=profile_id)


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GameSerializer
    lookup_field = 'id'

    def get_queryset(self):
        game_id = self.kwargs['game_id']
        return Game.objects.filter(id=game_id)

class UserGameDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserGameSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        game_id = self.kwargs['game_id']
        return UserGame.objects.filter(user_id=user_id and game_id=game_id)
