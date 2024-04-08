from django.urls import path
from .views import GameList, UserGameList, GameDetail, UserGameDetail, CreateUserView, LoginView, ProfileView, VerifyUserView


urlpatterns = [
        path('games/', GameList.as_view(), name='game-list'),
        path('games/usergames/<int:user_id>/', UserGameList.as_view(), name='user-game'),
        path('games/<int:game_id>/', GameDetail.as_view(), name='game-detail'),
        path('games/usergames/<int:profile_id>/<int:game_id>/', UserGameDetail.as_view(), name='user-game-detail'),
        path('user/register/', CreateUserView.as_view(), name='register'),
        path('user/login/', LoginView.as_view(), name='login'),
        path('user/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
        path('user/profile/', ProfileView.as_view(), name='users-profile'),
        ]
