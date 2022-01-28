from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomerRequestDeposit, CashDeposit,BankDeposit,MyPayments,Notifications
from django.conf import settings

User = settings.AUTH_USER_MODEL
from users.models import User


@receiver(post_save,sender=CustomerRequestDeposit)
def create_customer_request(sender,created,instance,**kwargs):
    title = f"New customer request from {instance.customer_phone}"
    message = f"{instance.customer_phone} just made a request of {instance.amount}"

    if created:
        Notifications.objects.create(user=instance.agent,notification_title=title,notification_message=message,customer=instance.customer_phone,user2=instance.agent,customer_request_slug=instance.slug)

@receiver(post_save,sender=CashDeposit)
def create_cash_request(sender,created,instance,**kwargs):
    title = f"New Cash Deposit from {instance.agent.username}"
    message = f"{instance.agent.username} just made a cash deposit of {instance.amount}"

    if created:
        Notifications.objects.create(user=instance.agent,notification_title=title,notification_message=message,user2=instance.guarantor,cash_deposit_request_slug=instance.slug)


@receiver(post_save, sender=BankDeposit)
def create_bank_request(sender, created, instance, **kwargs):
    title = f"New Bank Deposit from {instance.agent.username}"
    message = f"{instance.agent.username} just made a bank deposit of {instance.amount}"

    if created:
        Notifications.objects.create(user=instance.agent, notification_title=title, notification_message=message,
                                     user2=instance.guarantor, cash_deposit_request_slug=instance.slug)

@receiver(post_save,sender=MyPayments)
def create_payment(sender,created,instance,**kwargs):
    title = f"New payment from {instance.agent.username}"
    message = f"{instance.agent.username} just made a payment amount of {instance.amount}"
    admin_user = User.objects.get(id=1)

    if created:
        Notifications.objects.create(user=instance.agent, notification_title=title, notification_message=message,
                                     user2=admin_user, payment_slug=instance.slug)
