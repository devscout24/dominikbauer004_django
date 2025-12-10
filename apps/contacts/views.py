from django.shortcuts import render

# Create your views here.


from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import ContactAssignment, UserSelectedContact
from .serializers import ContactPersonSerializer, UserSelectContactSerializer
from apps.Authentication.views import BaseAPIView 
from django.contrib.auth import get_user_model
from rest_framework.response import Response

User= get_user_model


# class MyAssignedContactsView(BaseAPIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         contacts = ContactAssignment.objects.filter(owner=request.user)
#         serializer = ContactPersonSerializer(contacts, many=True)
#         return self.success_response("Available contact persons retrieved.", data=serializer.data)


# class SelectContactPersonView(BaseAPIView):
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request):
#         user = request.user
#         response_data = {}

#         # Assigned contact persons
#         try:
#             assignment = ContactAssignment.objects.get(owner=user)
#             assigned_serializer = ContactPersonSerializer(assignment)
#             response_data["assigned_contact_persons"] = assigned_serializer.data["contact_persons"]
#         except ContactAssignment.DoesNotExist:
#             response_data["assigned_contact_persons"] = []

#         # Selected contact person
#         selected_contact = UserSelectedContact.objects.filter(owner=user).first()
#         if selected_contact:
#             selected_serializer = UserSelectContactSerializer(selected_contact)
#             response_data["selected_contact_person"] = selected_serializer.data
#         else:
#             response_data["selected_contact_person"] = None

#         return Response({"message": "Contact info fetched successfully.", "data": response_data})

#     def post(self, request):
#         contact_id = request.data.get("contact_person")

#         if not contact_id:
#             return self.error_response("Contact person ID is required.")

#         # Get the contact assignment object for this user
#         try:
#             assignment = ContactAssignment.objects.get(owner=request.user)
#         except ContactAssignment.DoesNotExist:
#             return self.error_response("No contacts assigned to you.")

#         # Check if the selected contact is in the assigned list
#         if not assignment.contact_persons.filter(id=contact_id).exists():
#             return self.error_response("You can't select this contact person.")

#         # Create or update selection
#         selected_contact = assignment.contact_persons.get(id=contact_id)
#         selected_obj, created = UserSelectedContact.objects.update_or_create(
#             owner=request.user,
#             defaults={"selected_contact": selected_contact}
#         )

#         serializer = UserSelectContactSerializer(selected_obj)
#         msg = "Contact person selected successfully." if created else "Contact person updated successfully."
#         return self.success_response(msg, data=serializer.data)



# ================================
# 1️⃣ User’s available contact persons
# ================================
class MyAssignedContactsView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        contacts = request.user.contact_persons.all()
        serializer = ContactPersonSerializer(contacts, many=True)
        return self.success_response(
            "Available contact persons retrieved.",
            data=serializer.data
        )


# ================================
# 2️⃣ User selects or changes contact person
# ================================
class SelectContactPersonView(BaseAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # user-এর সব available contacts
        assigned = ContactPersonSerializer(
            user.contact_persons.all(),
            many=True
        ).data

        # selected contact
        selected = None
        if user.contact_person:
            selected = ContactPersonSerializer(user.contact_person).data

        return self.success_response(
            "Contact info fetched successfully.",
            data={
                "assigned_contact_persons": assigned,
                "selected_contact_person": selected
            }
        )

    def post(self, request):
        contact_id = request.data.get("contact_person")

        if not contact_id:
            return self.error_response("contact_person field is required.")

        user = request.user

        # নিশ্চিত করা যে contact_id user-এরই contact
        try:
            selected_contact = user.contact_persons.get(id=contact_id)
        except ContactPerson.DoesNotExist:
            return self.error_response("Invalid contact selection.")

        # update user.selected_contact (FK field)
        user.contact_person = selected_contact
        user.save()

        serializer = ContactPersonSerializer(selected_contact)

        return self.success_response(
            "Contact person selected successfully.",
            data=serializer.data
        )
