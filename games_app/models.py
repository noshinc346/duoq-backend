from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATUS = (
    ('PD', 'Played'),
    ('PG', 'Playing'),
    ('I', 'Interested')
)
class Game(models.Model):
    name = models.CharField(max_length=30)
    image = models.TextField()

    def __str__(self):
            return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    name = models.CharField(max_length=100)
    dob = models.DateField('DOB', null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile-pics', blank=True, null=True)
    banner = models.ImageField(upload_to='banners', blank=True, null=True)
    games = models.ManyToManyField(Game, through='UserGame')
    matches = models.ManyToManyField('self', through='Match', symmetrical=False)


    def __str__(self):
        return self.user.username
    

class UserGame(models.Model):
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS, default=STATUS[0][0])
    ign = models.CharField(max_length=30)
    rank = models.CharField(max_length=20)
    competitive = models.BooleanField()

    def __str__(self):
        return f'{self.profile_id.name} - {self.game_id.name}'


class Match(models.Model):
    user1_profile = models.ForeignKey(Profile, related_name='matches_as_user1', on_delete=models.CASCADE)
    user2_profile = models.ForeignKey(Profile, related_name='matches_as_user2', on_delete=models.CASCADE)

    def __str__(self):
        return f'Match between {self.user1_profile.user.username} and {self.user2_profile.user.username}'


