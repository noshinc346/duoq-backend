from django.db import models
from user_app.models import User

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

class UserGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS, default=STATUS[0][0])
    ign = models.CharField(max_length=30)
    rank = models.CharField(max_length=20)
    competitive = models.BooleanField()