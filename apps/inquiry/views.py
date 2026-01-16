from django.shortcuts import render
from apps.Authentication.views import BaseAPIView
from .serializers import InquiryImageSerializer, InquirySerializer,OfferDetailSerializer,UserSerializer
from .models import Inquiry, InquiryImage
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.contacts.models import UserSelectedContact
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from apps.User.models import CustomUser
# Create your views here.


class InquiryProfileView(BaseAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user   # CustomUser instance
            if not isinstance(user, CustomUser):
                return self.error_response("Profile not found")

            serializer = UserSerializer(user)
            return self.success_response(
                "Profile retrieved successfully",
                data=serializer.data
            )
        except CustomUser.DoesNotExist:    
            return self.error_response("Profile not found")
        except Exception as e:
            return self.error_response(f"Unexpected error: {str(e)}")


class OfferListAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        inquiries = Inquiry.objects.filter(
            user=user,
            is_approved=True,
            offer_pdf__isnull=False
        ).order_by('-created_at')

        serializer = InquirySerializer(inquiries, many=True, context={'request': request})
        return self.success_response("Offer list fetched successfully", serializer.data)

        

class OfferDetailAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        user = request.user

        # Authenticated user
        if user.is_authenticated:
            queryset = Inquiry.objects.filter(
                id=pk,  # ✅ এখন id ব্যবহার
                user=user,
                is_approved=True,
                offer_pdf__isnull=False
            )
        else:
            queryset = Inquiry.objects.filter(
                id=pk,
                is_approved=True,
                offer_pdf__isnull=False
            )

        inquiry = queryset.first()
        if not inquiry:
            return self.error_response("Offer not found or not approved yet.", status.HTTP_404_NOT_FOUND)

        serializer = InquirySerializer(inquiry, context={'request': request})
        return self.success_response("Offer details fetched successfully.", serializer.data)





class InquiryCreateAPIView(BaseAPIView):
    permission_classes = [IsAuthenticated]  # AllowAny এর বদলে IsAuthenticated দিবে
    parser_classes = [MultiPartParser, FormParser]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = request.user

        phone = request.data.get("phone")
        description = request.data.get("description", "")

        # ✅ Selected contact handling
        selected_contact = user.contact_person
        if not selected_contact:
            return self.error_response("No contact person selected for this user")

        # ✅ Save inquiry & images in atomic block
        inquiry = Inquiry.objects.create(
            user=user,
            phone=phone,
            description=description,
            contact_person=selected_contact
        )

        # Multiple images
        images = request.FILES.getlist('images')
        for img in images:
            InquiryImage.objects.create(inquiry=inquiry, image=img)

        serializer = InquirySerializer(inquiry, context={'request': request})

        return self.success_response(
            message="Inquiry submitted successfully!",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )