from django.db import models
from django.contrib.auth.models import User
# from games_app.models import Game, UserGame
# from games_app.serializers import GameSerializer, UserGameSerializer


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    name = models.CharField(max_length=100)
    dob = models.DateField('DOB', null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile-pics', blank=True, null=True)
    banner = models.ImageField(upload_to='banners', blank=True, null=True)
    # Removed direct ManyToManyField relationship with Game
    matches = models.ManyToManyField('self', through='Match', symmetrical=False)

    def __str__(self):
        return self.user.username

class Match(models.Model):
    user1_profile = models.ForeignKey(Profile, related_name='matches_as_user1', on_delete=models.CASCADE)
    user2_profile = models.ForeignKey(Profile, related_name='matches_as_user2', on_delete=models.CASCADE)
    recipricated = models.BooleanField(default=False)

    def __str__(self):
        return f'Match between {self.user1_profile.user.username} and {self.user2_profile.user.username}'




