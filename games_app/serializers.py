from rest_framework import serializers
from .models import Game, UserGame
from user_app.models import User
from user_app.serializers import ProfileSerializer
from rest_framework.validators import UniqueTogetherValidator

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
        validators = [
                UniqueTogetherValidator(
                    queryset = Game.objects.all(),
                    fields = ['name'],
                    message = "you already have this game in the libarary"
                    )
                ]

class UserGameSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(many=True, read_only=True)
    game = GameSerializer(many=True, read_only=True)

    class Meta:
        model = UserGame
        fields = '__all__'
        validators = [
                UniqueTogetherValidator(
                    queryset = UserGame.objects.all(),
                    fields = ['profile_id', 'game_id'],
                    message = "you already have this game in your libarary"
                    )
                ]
