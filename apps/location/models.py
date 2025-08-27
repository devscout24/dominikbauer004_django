from django.conf import settings 
from django.db import models


class Location(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="locations")
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.address} - {self.user.customer_number}"

    class Meta:
        verbose_name_plural = "Delivery Locations"
