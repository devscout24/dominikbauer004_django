from django.urls import path
from .views import NewsPortalListView, UserNewsView

urlpatterns = [
    path("list/", NewsPortalListView.as_view(), name="all-news-list"),
     path("<int:pk>/", UserNewsView.as_view(), name="news-detail"), 
]
