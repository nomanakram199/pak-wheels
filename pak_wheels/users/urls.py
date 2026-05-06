from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import UserRegistrationView, ProfileView, UserTokenObtainPairView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserTokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
]