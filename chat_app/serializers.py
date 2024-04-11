from django.contrib.auth.models import User
from .models import Chat, Message
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
        validators = [
                UniqueTogetherValidator(
                    queryset = Chat.objects.all(),
                    fields = ['user1', 'user2'],
                    message = 'These two users already have a chat'
                    )
                ]

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
