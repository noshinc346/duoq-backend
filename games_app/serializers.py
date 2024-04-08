from rest_framework import serializers
from .models import Game, UserGame, Profile, Match
from django.contrib.auth.models import User

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  

    class Meta:
        model = User
        fields = ('id', 'username', 'email')
    
    def create(self, validated_data):
      user = User.objects.create_user(
          username=validated_data['username'],
          email=validated_data['email'],
          password=validated_data['password']  
      )
      
      return user
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserGameSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(many=True, read_only=True)
    game = GameSerializer(many=True, read_only=True)

    class Meta:
        model = UserGame
        fields = '__all__'

