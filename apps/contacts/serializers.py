

from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User= get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "customer_number", "name", "email", "phone"]

class ContactPersonSerializer(serializers.ModelSerializer):
    contact_persons = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ContactAssignment
        fields = ["id", "contact_persons"]




   
        
class UserSelectContactSerializer(serializers.ModelSerializer):
    selected_contact = UserSerializer(read_only=True)

    class Meta:
        model = UserSelectedContact
        fields = ["selected_contact"]


