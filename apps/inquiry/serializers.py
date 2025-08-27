from rest_framework import serializers
from .models import InquiryImage, Inquiry
from apps.contacts.serializers import UserSelectContactSerializer  
from apps.User.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'customer_number','name', 'company_name', 'email', 'phone']

class InquiryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InquiryImage
        fields = ['id', 'image']

class InquirySerializer(serializers.ModelSerializer):
    title = serializers.CharField(read_only=True) 
    company_name = serializers.CharField(source='user.company_name', read_only=True)
    name = serializers.CharField(source='user.name', read_only=True)
 
    contact_person = serializers.SerializerMethodField()
    
    images = InquiryImageSerializer(many=True, read_only=True)
    offer_pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = Inquiry
        fields = [
            'id', 'offer_number', 'created_at',
            'company_name', 'name', 'phone', 'title', 'description',
            'contact_person', 'images', 'offer_pdf_url'
        ]

    def get_contact_person(self, obj):
        if obj.contact_person:
            return {
                "id": obj.contact_person.id,
                "name": obj.contact_person.name,
                "email": obj.contact_person.email,
                "phone": obj.contact_person.phone
            }
        return None

    def get_offer_pdf_url(self, obj):
        request = self.context.get('request')
        if obj.offer_pdf:
            return request.build_absolute_uri(obj.offer_pdf.url)
        return None


class OfferDetailSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='user.company_name', read_only=True)
    name = serializers.CharField(source='user.name', read_only=True)

    contact_person_name = serializers.CharField(source='contact_person.name', read_only=True)
    contact_person_email = serializers.EmailField(source='contact_person.email', read_only=True)
    contact_person_phone = serializers.CharField(source='contact_person.phone', read_only=True)

    images = InquiryImageSerializer(many=True, read_only=True)
    offer_pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = Inquiry
        fields = [
            'id', 'offer_number', 'created_at',
            'company_name', 'name', 'phone', 'description',
            'contact_person_name', 'contact_person_email', 'contact_person_phone',
            'images', 'offer_pdf_url'
        ]

    def get_offer_pdf_url(self, obj):
        request = self.context.get('request')
        if obj.offer_pdf and request:
            return request.build_absolute_uri(obj.offer_pdf.url)
        return None