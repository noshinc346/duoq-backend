from rest_framework import serializers
from .models import Game, UserGame
from user_app.models import User, Profile
from user_app.serializers import ProfileSerializer
from rest_framework.validators import UniqueTogetherValidator
from django.core.exceptions import ObjectDoesNotExist

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
    profile = ProfileSerializer(read_only=True)
    game = GameSerializer(read_only=True)
    profile_id = serializers.IntegerField(write_only=True)
    game_id = serializers.IntegerField(write_only=True)


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

    def create(self, validated_data):
        # Fetch the Profile and Game instances using the provided IDs
        profile = Profile.objects.get(pk=validated_data.pop('profile_id'))
        game = Game.objects.get(pk=validated_data.pop('game_id'))

        # Create and return the UserGame instance
        user_game = UserGame.objects.create(profile=profile, game=game, **validated_data)
        return user_game
