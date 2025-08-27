
from django.urls import path, include
from .views import UserProfileInfoView


urlpatterns = [
    path('profile/', UserProfileInfoView.as_view(), name='user-profile'),
]