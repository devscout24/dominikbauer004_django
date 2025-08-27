from rest_framework import serializers
from .models import Location
from apps.User.models import CustomUser

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class UserDeliveryLocationSerializer(serializers.ModelSerializer):
    delivery_location = LocationSerializer(read_only=True)
    delivery_location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        source='delivery_location',
        write_only=True
    )

    class Meta:
        model = CustomUser
        fields = ['delivery_location', 'delivery_location_id']
