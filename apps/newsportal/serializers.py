from rest_framework import serializers
from .models import NewsPortal


class NewsPortalSerializer(serializers.ModelSerializer):
    banner = serializers.ImageField(use_url=True)
    pdf_file = serializers.FileField(use_url=True)
    class Meta:
        model = NewsPortal
        fields = ['id','user', 'title', 'issue_number', 'issue_date', 'banner','pdf_file', 'external_link']
