from django.urls import path
from .views import InquiryCreateAPIView, OfferListAPIView, OfferDetailAPIView, InquiryProfileView

urlpatterns = [
    path('create/', InquiryCreateAPIView.as_view(), name='inquiry-create'),
    path('offers/', OfferListAPIView.as_view(), name='offer-list'),
    path('offers/<int:pk>/', OfferDetailAPIView.as_view(), name='offer-detail'),
    path('profile/', InquiryProfileView.as_view(), name='profile-inquiry'),
]
