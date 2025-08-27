from rest_framework import serializers
from apps.User.models import CustomUser
from .models import PasswordResetRequest

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model= CustomUser
        fields = ('customer_number', 'password')
        extra_kwargs ={
            'password': {'write_only': True, }
        }
    
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)   
    
    
    
class PasswordResetRequestSerializer(serializers.ModelSerializer):
    customer_number = serializers.CharField(write_only=True)

    class Meta:
        model = PasswordResetRequest
        fields = ('customer_number', 'reviewed', 'requested_at', 'completed', 'completed_at')
        read_only_fields = ('requested_at', 'completed_at')

    def validate_customer_number(self, value):
        try:
            user = CustomUser.objects.get(customer_number=value)
        except user.DoesNotExist:
            raise serializers.ValidationError("User with this customer number does not exist.")
        return value

    def create(self, validated_data):
        customer_number = validated_data.pop('customer_number')
        user = CustomUser.objects.get(customer_number=customer_number)
        
        return PasswordResetRequest.objects.create(
            user=user,
            **validated_data
        )