from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.contacts.models import ContactAssignment, UserSelectedContact
from apps.Authentication.views import BaseAPIView
from apps.contacts.serializers import ContactPersonSerializer, UserSelectContactSerializer
from apps.location.serializers import LocationSerializer, UserDeliveryLocationSerializer
from .serializers import UserInfoSerializer
from .models import CustomUser
from apps.location.models import Location


class UserProfileInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            response_data = {}

            # ------------------------
            # User Info
            # ------------------------
            try:
                user_serializer = UserInfoSerializer(user)
                response_data["user_info"] = user_serializer.data
            except Exception as e:
                response_data["user_info"] = {}

            # ------------------------
            # Assigned Contact Persons
            # ------------------------
            try:
                assignment = getattr(user, "assigned_contacts", None)  # related_name
                if assignment:
                    assigned_serializer = ContactPersonSerializer(assignment)
                    response_data["assigned_contact_persons"] = assigned_serializer.data.get('contact_persons', [])
                else:
                    response_data["assigned_contact_persons"] = []
            except Exception as e:
                response_data["assigned_contact_persons"] = []

            # ------------------------
            # Selected Contact Person
            # ------------------------
            try:
                selected_contact = getattr(user, "selected_contact", None)
                if selected_contact:
                    selected_serializer = UserSelectContactSerializer(selected_contact)
                    response_data["selected_contact_person"] = selected_serializer.data.get('selected_contact', None)
                else:
                    response_data["selected_contact_person"] = None
            except Exception as e:
                response_data["selected_contact_person"] = None

            # ------------------------
            # All Locations (assigned to user)
            # ------------------------
            try:
                all_locations = Location.objects.filter(user=user)
                location_serializer = LocationSerializer(all_locations, many=True)
                response_data["assigned_locations"] = location_serializer.data
            except Exception as e:
                response_data["assigned_locations"] = []

            # ------------------------
            # Selected Location
            # ------------------------
            try:
                if hasattr(user, 'delivery_location') and user.delivery_location:
                    selected_location_serializer = LocationSerializer(user.delivery_location)
                    response_data["selected_location"] = selected_location_serializer.data
                else:
                    response_data["selected_location"] = None
            except Exception as e:
                response_data["selected_location"] = None

            # ------------------------
            # Final Response
            # ------------------------
            return Response({
                "success": True,
                "message": "User profile info fetched successfully",
                "status_code": 200,
                "data": response_data
            })

        except Exception as e:
            return Response({
                "success": False,
                "message": "Something went wrong while fetching user profile info",
                "status_code": 500,
                "error": str(e),
                "data": {}
            })



