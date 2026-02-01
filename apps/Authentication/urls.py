from django.urls import path
from .views import RegisterView, LoginView, RequestPasswordResetView, LogoutView, DeleteAccountAPIView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('request-password-reset/', RequestPasswordResetView.as_view(), name='request-password-reset'),

    # Command: Permanently delete authenticated user's account
    path("delete-account/", DeleteAccountAPIView.as_view(), name="delete-account"),
]
