from django.contrib import admin
from .models import Game, UserGame, Profile

# Register your models here.
admin.site.register(Game)
admin.site.register(UserGame)
admin.site.register(Profile)

