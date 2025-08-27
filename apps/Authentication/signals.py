# signals.py
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from apps.User.models import CustomUser
from .models import PasswordResetRequest
from django.utils import timezone

@receiver(post_save, sender=CustomUser)
def send_activation_email(sender, instance, created, **kwargs):
    """
    Send activation email when user is activated by admin
    """
    if not created and instance.is_active and instance._previous_active != instance.is_active:
        subject = 'Your Account Has Been Activated'
        message = f"""
        Dear User,

        Your account (Customer Number: {instance.customer_number}) has been activated.

        You can now login to the system using your credentials:
        - Customer Number: {instance.customer_number}
        - Username: {instance.email or instance.customer_number}

        Login URL: {settings.FRONTEND_LOGIN_URL}

        If you didn't request this activation or need any assistance, 
        please contact our support team at {settings.SUPPORT_EMAIL}.

        Best regards,
        {settings.SITE_NAME} Team
        """
        
        send_mail(
            subject,
            message.strip(), 
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )
        



@receiver(post_save, sender=PasswordResetRequest)
def send_reset_request_notification(sender, instance, created, **kwargs):
    if created:
        # Email to user
        send_mail(
            subject="Password Reset Request Received",
            message=f"""
            Dear {instance.user.name or instance.user.customer_number},
            
            Your password reset request has been received.
            Our admin team will process it within 24 hours.
            
            Customer Number: {instance.user.customer_number}
            Request Time: {instance.requested_at.strftime('%Y-%m-%d %H:%M')}
            
            {settings.SITE_NAME} Team
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.user.email],
            fail_silently=False
        )


@receiver(post_save, sender=CustomUser)
def send_password_change_notification(sender, instance, **kwargs):
    if hasattr(instance, '_password_changed') and instance._password_changed:
        reset_request = PasswordResetRequest.objects.filter(
             user=instance,
            reviewed=True,
            completed=False
        ).first()
        
        if reset_request:
            # Email to user with new password
            send_mail(
                subject="Your Password Has Been Reset",
                message=f"""
                Dear {instance.name or instance.customer_number},
                
                Your password has been reset by admin.
                
                New temporary credentials:
                Customer Number: {instance.customer_number}
                New Password: {instance._new_password}
                
                Please login at: {settings.FRONTEND_LOGIN_URL}
                
                For security, please change your password after login.
                
                {settings.SITE_NAME} Team
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=False
            )
            
            # Mark request as completed
            reset_request.completed = True
            reset_request.completed_at = timezone.now()
            reset_request.save()