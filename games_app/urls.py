from django.urls import path
from .views import GameList, GamesInterestedList, GamesPlayingList

urlpatterns = [
        path('games-provided/', GameList.as_view(), name='game-list'),
        path('games-interested/<int:user_id>/', GamesInterestedList.as_view(), name='games-interested'),
        path('games-playing/<int:user_id>/', GamesPlayingList.as_view(), name='games-playing'),
        ]
