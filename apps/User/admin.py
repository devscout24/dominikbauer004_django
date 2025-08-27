from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.location.models import Location
from .models import CustomUser

class LocationInline(admin.TabularInline):
    model = Location
    fields = ["address"]
    extra = 1   # সবসময় অন্তত ১টা খালি row দেখাবে


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    inlines = [LocationInline]   # ✅ Inline যুক্ত হলো

    list_display = (
        'customer_number', 'company_name', 'email', 'phone',
        'is_active', 'is_staff', 'is_superuser'
    )

    fieldsets = (
        (None, {
            'fields': (
                'customer_number', 'company_name', 'name',
                'email', 'phone', 'billing_location', 'password'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'customer_number','company_name','name','email',
                'phone','billing_location','password1','password2',
                'is_active','is_staff','is_superuser',
                'groups','user_permissions',
            ),
        }),
    )

    search_fields = ('customer_number','company_name','email','phone')
    ordering = ('customer_number',)

