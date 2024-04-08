from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    name = models.CharField(max_length=100)
    dob = models.DateField('DOB')
    profile_picture = models.ImageField(upload_to='profile-pics', blnak=True, null=True)
    banner = models.ImageField(upload_to='banners', blnak=True, null=True)
    games = models.ManyToManyField(Game, through='UserGame')
    matches = models.ManyToManyField('self', through='Match', symmetrical=False)


    def __str__(self):
        return self.user.username
    

class Match(models.Model):
    user1_profile = models.ForeignKey(Profile, related_name='matches_as_user1', on_delete=models.CASCADE)
    user2_profile = models.ForeignKey(Profile, related_name='matches_as_user2', on_delete=models.CASCADE)

    def __str__(self):
        return f'Match between {self.user1_profile.user.username} and {self.user2_profile.user.username}'




