from django.urls import path
from .views import CreateUserView, LoginView, VerifyUserView

urlpatterns = [
  path('register/', CreateUserView.as_view(), name='register'),
  path('login/', LoginView.as_view(), name='login'),
  path('token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
]
