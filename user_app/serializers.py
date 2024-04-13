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
    def __init__(self, *args, **kwargs):
        super(MatchSerializer, self).__init__(*args, **kwargs)
        # Make fields writable conditionally based on the request type (check for 'view' and 'request' in context)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.fields['user1_profile'] = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
            self.fields['user2_profile'] = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
        else:
            self.fields['user1_profile'] = ProfileSerializer(read_only=True)
            self.fields['user2_profile'] = ProfileSerializer(read_only=True)

    class Meta:
        model = Match
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Match.objects.all(),
                fields=['user1_profile', 'user2_profile'],
                message="You already have this match in your library"
            )
        ]

    def create(self, validated_data):
        match = Match.objects.create(**validated_data)
        return match


class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = '__all__'
