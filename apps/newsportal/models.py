from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
# Create your models here.

User= get_user_model()

class NewsPortal(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="news_portal")
    title= models.CharField(max_length=400)
    issue_number= models.PositiveBigIntegerField()
    issue_date= models.DateField()
    banner= models.ImageField(upload_to="beton-news/")
    pdf_file = models.FileField(upload_to="beton-news/pdfs/")
    external_link= models.URLField(blank=True, null=True)
    created_by= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering= ["-issue_date"]
        
    def __str__(self):
        return f"{self.title} ({self.issue_number})"