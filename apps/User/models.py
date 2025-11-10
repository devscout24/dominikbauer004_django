from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

import random 
from django.db import models
from .manager import CustomUserManager
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from apps.location.models import Location
from apps.contacts.models import UserSelectedContact
# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    customer_number = models.CharField(max_length=20, unique=True)
    company_name = models.CharField(max_length=500, blank=True)
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    billing_location = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Status field for user management
    STATUS_CHOICES = (
        ('new', 'New User'),  # Not active yet
        ('active', 'Custom User'),  # Active user
        ('inactive', 'Inactive'),
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='new'
    )

    # Single delivery location
    delivery_location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users_with_delivery_location"
    )
    contact_person = models.ForeignKey(
        UserSelectedContact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_selected_contact_person"
    )

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'customer_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    class Meta:
        ordering = ['created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._previous_active = getattr(self, 'is_active', False)

    def set_password(self, raw_password):
        super().set_password(raw_password)
        self._password_changed = True
        self._new_password = raw_password

    def save(self, *args, **kwargs):
        # Auto update status based on is_active
        if self.is_active and self.status == 'new':
            self.status = 'active'
        elif not self.is_active and self.status == 'active':
            self.status = 'inactive'
            
        # Store previous active status before saving
        if self.pk:
            try:
                old_user = CustomUser.objects.get(pk=self.pk)
                self._previous_active = old_user.is_active
            except CustomUser.DoesNotExist:
                self._previous_active = self.is_active
        else:
            self._previous_active = self.is_active
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.customer_number