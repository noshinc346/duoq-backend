from django.urls import path
from .views import GameList, UserGameList, GameDetail, UserGameDetail


urlpatterns = [
        path('', GameList.as_view(), name='game-list'),
        path('usergames/<int:user_id>/', UserGameList.as_view(), name='user-game'),
        path('<int:game_id>/', GameDetail.as_view(), name='game-detail'),
        path('usergames/<int:user_id>/<int:game_id>/', UserGameDetail.as_view(), name='user-game-detail'),
        ]
