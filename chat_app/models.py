from django.db import models
from user_app.models import Profile

# Create your models here.

class Chat(models.Model):
    user1 = models.ForeignKey(Profile, related_name='first_user', on_delete=models.CASCADE)
    user2 = models.ForeignKey(Profile, related_name='second_user', on_delete=models.CASCADE)

    def __str__(self):
        return f'chat between {self.user1} and {self.user2}'


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='chat', on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.time} - {self.content}'
