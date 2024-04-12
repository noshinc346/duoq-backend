from django.contrib.auth.models import User
from .models import Profile, Match, Preference
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

#User serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
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


class MatchSerializer(serializers.ModelSerializer):
    user1_profile = ProfileSerializer(read_only=True)
    user2_profile = ProfileSerializer(read_only=True)
    user1_profile_id = serializers.IntegerField(write_only=True)
    user2_profile_id = serializers.IntegerField(write_only=True)


    class Meta:
        model = Match
        fields = '__all__'
        validators = [
                UniqueTogetherValidator(
                    queryset = Match.objects.all(),
                    fields = ['user1_profile', 'user2_profile'],
                    message = "you already have this match in your libarary"
                    )
                ]

    def create(self, validated_data):
        # Fetch the Profile and Game instances using the provided IDs
        user1_profile = Profile.objects.get(pk=validated_data.pop('user1_profile_id'))
        user2_profile = Profile.objects.get(pk=validated_data.pop('user2_profile_id'))

        # Create and return the UserGame instance
        match = Match.objects.create(user1_profile=user1_profile, user2_profile=user2_profile, **validated_data)
        return match

class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = '__all__'






        
