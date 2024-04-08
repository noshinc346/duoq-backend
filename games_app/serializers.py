from rest_framework import serializers
from .models import Game, UserGame
from user_app.models import User
from user_app.serializers import ProfileSerializer

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class UserGameSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(many=True, read_only=True)
    game = GameSerializer(many=True, read_only=True)

    class Meta:
        model = UserGame
        fields = '__all__'