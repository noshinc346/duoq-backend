from django.urls import path
from .views import GameList, UserGameList, GameDetail, UserGameDetail, Home, UserGamesList


urlpatterns = [
        path('games', GameList.as_view(), name='game-list'),
        path('games/usergames/<int:user_id>/', UserGameList.as_view(), name='user-game'),
        path('games/<int:id>/', GameDetail.as_view(), name='game-detail'),
        path('games/usergames/detail/<int:game_id>/', UserGameDetail.as_view(), name='user-game-detail'),
        path('', Home.as_view(), name='home'),
        path('games/usergames/for/<int:game_id>/', UserGamesList.as_view(), name='usergames-list'),
]
