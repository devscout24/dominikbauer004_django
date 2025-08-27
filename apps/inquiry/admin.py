from django.contrib import admin
from .models import Inquiry, InquiryImage


class InquiryImageInline(admin.TabularInline):
    model = InquiryImage
    extra = 0
    readonly_fields = ['image']  # শুধু show হবে
    
    

class InquiryImageInline(admin.TabularInline):
    model = InquiryImage
    extra = 0

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['offer_number', 'title',  'user', 'phone', 'contact_person', 'is_approved', 'created_at', 'offer_pdf']
    search_fields = ['offer_number', 'user__name', 'user__company_name', 'phone']
    list_filter = ['is_approved', 'contact_person', 'created_at']
    readonly_fields = ['offer_number']
    inlines = [InquiryImageInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superuser sees all
        return qs.filter(contact_person=request.user)  # Staff sees only their inquiries

    def get_readonly_fields(self, request, obj=None):
        fields = list(self.readonly_fields)
        if not request.user.is_superuser:
            # Staff can't edit user/contact_person
            fields += ['offer_number', 'user', 'phone', 'contact_person', 'created_at']  # Staff will still upload PDF
        return fields
