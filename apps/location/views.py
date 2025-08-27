from django.shortcuts import render
from apps.Authentication.views import BaseAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserDeliveryLocationSerializer, LocationSerializer
from .models import Location

# Create your views here.
class UserSelectLocationView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        serializer = UserDeliveryLocationSerializer(
            user,
            data=request.data,
            partial=True,
            context={'request': request}  # for filtering inside serializer if needed
        )

        # Optional: restrict the location to the user's own locations
        delivery_location_id = request.data.get('delivery_location_id')
        if delivery_location_id:
            if not Location.objects.filter(id=delivery_location_id, user=user).exists():
                return self.error_response(
                    "Invalid location. You can only select your own locations.",
                    data={}
                )

        if serializer.is_valid():
            serializer.save()
            return self.success_response(
                "Location selected successfully.",
                data=serializer.data
            )

        return self.error_response("Not Updated", serializer.errors)



class AllLocationView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Return all locations for the current user
        locations = Location.objects.filter(user=request.user)
        serializer = LocationSerializer(locations, many=True)
        return self.success_response(
            "Locations retrieved successfully",
            data=serializer.data
        )
