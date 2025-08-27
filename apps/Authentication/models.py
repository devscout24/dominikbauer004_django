from django.db import models

from django.utils import timezone
from django.conf import settings
# Create your models here.
from datetime import timedelta

class PasswordResetRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reviewed= models.BooleanField(default=False)
    reviewed_by= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, null=True, blank=True, related_name="request_review")
    requested_at= models.DateTimeField(auto_now_add=True)
    completed= models.BooleanField(default=False)
    completed_at= models.DateTimeField(blank=True, null=True)
    
    def is_expired(self):
        """Check if request is older than 24 hours"""
        return (timezone.now() - self.requested_at) > timedelta(hours=24)
    
    def __str__(self):
        status = "completed" if self.completed else "pending"
        return f"Reset request for {self.user.customer_number} ({status})"

