from rest_framework import serializers
from apps.User.models import CustomUser
from .models import PasswordResetRequest, RegistrationRequest

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('customer_number',)

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            customer_number=validated_data['customer_number'],
            is_active=False  # inactive until admin edits
        )


class PasswordResetRequestSerializer(serializers.ModelSerializer):
    customer_number = serializers.CharField(write_only=True)

    class Meta:
        model = PasswordResetRequest
        fields = ('customer_number', 'reviewed', 'reviewed_by', 'requested_at', 'completed', 'completed_at')
        read_only_fields = ('reviewed', 'reviewed_by', 'requested_at', 'completed', 'completed_at')

    def create(self, validated_data):
        customer_number = validated_data.pop('customer_number')
        try:
            user = CustomUser.objects.get(customer_number=customer_number)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(f"User with customer_number {customer_number} does not exist")
        
        # Ensure 'user' is not in validated_data
        validated_data.pop('user', None)  # remove if exists

        return PasswordResetRequest.objects.create(user=user, **validated_data)

