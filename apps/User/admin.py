from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.location.models import Location
from .models import CustomUser, ContactPerson


class ContactPersonInline(admin.TabularInline):
    model = ContactPerson
    extra = 1
    fields = ['full_name', 'email', 'phone', 'designation', 'notes']


class LocationInline(admin.TabularInline):
    model = Location
    fields = ["address"]
    extra = 1


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    inlines = [ContactPersonInline, LocationInline]

    # ---- FIXED ----
    list_display = (
        'customer_number', 'company_name', 'email', 'phone',
        'is_active', 'is_staff', 'is_superuser', 'created_at'
    )

    list_filter = ('is_active', 'is_staff', 'is_superuser', 'created_at')

    # ---- FIXED: Removed duplicate fieldsets ----
    fieldsets = (
        (None, {
            'fields': (
                'customer_number', 'company_name', 'name',
                'email', 'phone', 'billing_location', 'password'
            )
        }),
        ('Delivery & Contact', {
            'fields': (
                'delivery_location', 'contact_person'
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

    search_fields = ('customer_number', 'company_name', 'email', 'phone')
    ordering = ('customer_number',)
