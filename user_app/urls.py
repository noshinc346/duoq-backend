from django.urls import path
from .views import CreateUserView, LoginView, VerifyUserView, ProfileView, ProfileDetail, MatchList, MatchDetail

urlpatterns = [
        path('register/', CreateUserView.as_view(), name='register'),
        path('login/', LoginView.as_view(), name='login'),
        path('token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
        path('profile/', ProfileView.as_view(), name='users-profile'),
        path('profile/<int:id>/', ProfileDetail.as_view(), name='others-profile'),
        path('matches/', MatchList.as_view(), name='users-matches'),
        path('matches/<int:id>/', MatchDetail.as_view(), name='match')
        ]
