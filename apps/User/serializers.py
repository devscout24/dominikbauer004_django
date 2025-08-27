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