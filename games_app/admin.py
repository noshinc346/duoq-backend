from django.contrib import admin
from .models import Game, UserGame

# Register your models here.
admin.site.register(Game)
admin.site.register(UserGame)
