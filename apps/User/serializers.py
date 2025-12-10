from rest_framework import serializers
from .models import CustomUser


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'id', 'customer_number', 'company_name', 'name', 
            'email', 'phone', 'billing_location', 
            'delivery_location', 'contact_person'
        ]


class ContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPerson
        fields = ["id", "full_name", "email", "phone", "designation", "notes"]


class UserSelectedContactSerializer(serializers.ModelSerializer):
    selected_contact = ContactPersonSerializer(source='contact_person')

    class Meta:
        model = User
        fields = ["selected_contact"]