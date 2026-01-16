import uuid
from django.db import models
from django.conf import settings
from apps.User.models import ContactPerson


def inquiry_image_path(instance, filename):
    # Example: inquiries/<offer_number>/<filename>
    return f"inquiries/{instance.inquiry.offer_number}/{filename}"

class Inquiry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inquiries')
    phone = models.CharField(max_length=15, blank=True, null=True)
    title= models.CharField(max_length=455)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    offer_number = models.CharField(max_length=20, unique=True, editable=False)
    contact_person = models.ForeignKey(
        ContactPerson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contact_inquiries',
    )

    # Staff uploaded offer
    offer_pdf = models.FileField(upload_to="offers/pdfs/", blank=True, null=True)

    # ✅ New field for staff approval
    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        import uuid
        if not self.offer_number:
            self.offer_number = str(uuid.uuid4().int)[:6]
        # Auto select contact if not manually set
        if not self.contact_person and self.user.contact_person:
            self.contact_person = self.user.contact_person
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Offer {self.offer_number} - {self.user.company_name}"


class InquiryImage(models.Model):
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=inquiry_image_path)

    def __str__(self):
        return f"Image for {self.inquiry.offer_number}"
