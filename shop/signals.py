# shop/signals.py
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order  # Assuming this is the correct model

@receiver(post_save, sender=Order)
def send_order_notification(sender, instance, created, **kwargs):
    if created:  # Only send email for new orders
        subject = f"New Order Notification: Order #{instance.id}"
        
        # Update with correct field name for customer
        message = (
            f"An order has been placed with the following details:\n\n"
            f"Order ID: {instance.id}\nCustomer: {instance.customer}\n"  # Use actual field
            f"Total Amount: {instance.total_price}\n\n"
            "Please review this order in the admin panel for more details: portal.msplantspares.ie/admin"
        )

        # Combined recipient list as a single argument
        recipient_list = ['scahill@msplantspares.ie', 'dmanning@msplantspares.ie']

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
