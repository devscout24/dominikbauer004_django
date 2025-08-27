from django.contrib import admin
from .models import ContactAssignment, UserSelectedContact
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

# @admin.register(ContactAssignment)
# class ContactAssignmentAdmin(admin.ModelAdmin):
#     list_display = ['owner', 'contact_person']

#     def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
#         if db_field.name == "contact_person":
#             kwargs["queryset"] = CustomUser.objects.filter(is_staff=True) | CustomUser.objects.filter(is_superuser=True)
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)

# @admin.register(UserSelectedContact)
# class UserSelectedContactAdmin(admin.ModelAdmin):
#     list_display = ['owner', 'selected_contact']


@admin.register(ContactAssignment)
class ContactAssignmentAdmin(admin.ModelAdmin):
    list_display = ['owner']
    filter_horizontal = ('contact_persons',) 
