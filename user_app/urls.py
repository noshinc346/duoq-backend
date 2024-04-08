from django.urls import path
from .views import CreateUserView, LoginView, VerifyUserView, ProfileView

urlpatterns = [
  path('register/', CreateUserView.as_view(), name='register'),
  path('login/', LoginView.as_view(), name='login'),
  path('token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
  path('profile/', ProfileView.as_view(), name='profile'),
]
