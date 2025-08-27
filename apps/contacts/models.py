from django.db import models
from rest_framework.exceptions import ValidationError
from django.conf import settings
# Create your models here.


# class ContactAssignment(models.Model):
#     owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assigned_contacts")
#     contact_persons = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="assigned_to_owners", limit_choices_to={'is_staff': True})

#     def clean(self):
#         if not (self.contact_person.is_staff or self.contact_person.is_superuser):
#             raise ValidationError("Only staff or superusers can be contact persons.")

#     def __str__(self):
#         return f"{self.contact_person.name} assigned to {self.owner.name}"


class UserSelectedContact(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="selected_contact")
    selected_contact = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chosen_by_user")

    def __str__(self):
        return f"{self.owner.name} ({self.owner.customer_number}) selected {self.selected_contact.name} ({self.selected_contact.email})"


class ContactAssignment(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assigned_contacts")
    contact_persons = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="assigned_to_owners", limit_choices_to={'is_staff': True})

    def __str__(self):
        contacts = ", ".join([f"{c.name} ({c.email} - {c.customer_number})" for c in self.contact_persons.all()])
        return f"Contacts assigned to {self.owner.name}: {contacts}"


