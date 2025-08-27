
from django.contrib.auth.base_user import BaseUserManager



class CustomUserManager(BaseUserManager):
    def create_user(self, customer_number, password=None, **extra_fields):
        if not customer_number:
            raise ValueError("Customer number is required")
        user = self.model(customer_number=customer_number, **extra_fields)
        user.set_password(password)
        user.is_active = extra_fields.get('is_active', False)
        user.save(using=self._db)
        return user


    def create_superuser(self, customer_number, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(customer_number, password, **extra_fields)
