from rest_framework import serializers
from apps.User.models import CustomUser
from .models import PasswordResetRequest, RegistrationRequest

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationRequest
        fields = ('customer_number',)

    def create(self, validated_data):
        # Save a pending registration request
        return RegistrationRequest.objects.create(**validated_data)



class PasswordResetRequestSerializer(serializers.ModelSerializer):
    customer_number = serializers.CharField(write_only=True)

    class Meta:
        model = PasswordResetRequest
        fields = ('customer_number', 'reviewed', 'reviewed_by', 'requested_at', 'completed', 'completed_at')
        read_only_fields = ('reviewed', 'reviewed_by', 'requested_at', 'completed', 'completed_at')

    def create(self, validated_data):
        # user must be passed from view
        user = validated_data.pop('user')
        return PasswordResetRequest.objects.create(user=user, **validated_data)