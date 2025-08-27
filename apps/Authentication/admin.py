from django.contrib import admin

# Register your models here.

from .models import PasswordResetRequest

@admin.register(PasswordResetRequest)
class PasswordResetRequestAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'reviewed', 'completed', 'reviewed_by', 'requested_at',
        'completed_at', 'is_expired_display'
    )
    list_filter = ('reviewed', 'reviewed_by')
    search_fields = ('user__customer_number', 'user__email', 'user__name')
    readonly_fields = ('reviewed_by',)

    def is_expired_display(self, obj):
        return obj.is_expired()
    is_expired_display.short_description = 'Expired'
    is_expired_display.boolean = True

    def save_model(self, request, obj, form, change):
        if obj.reviewed and not obj.reviewed_by:
            obj.reviewed_by = request.user
        super().save_model(request, obj, form, change)