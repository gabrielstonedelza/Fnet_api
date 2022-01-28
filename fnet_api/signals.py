from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomerRequestDeposit, CashDeposit,BankDeposit,MyPayments,Notifications
from django.conf import settings

User = settings.AUTH_USER_MODEL


@receiver(post_save,sender=CustomerRequestDeposit)
def create_customer_request(sender,created,instance,**kwargs):
    title = f"New customer request from {instance.customer_phone}"
    message = f"{instance.customer_phone} just made a request of {instance.amount}"
    
    if created:
        Notifications.objects.create(user=instance.user,notification_title=title,notification_message=message,customer=instance.customer_phone,user2=instance.agent,customer_request_slug=instance.slug)