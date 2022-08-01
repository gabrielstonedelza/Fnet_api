from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomerRequestDeposit, ExpensesRequest, BankDeposit, MyPayments, Notifications, OTP, \
    CustomerPaymentAtBank
from django.conf import settings

User = settings.AUTH_USER_MODEL
from users.models import User


@receiver(post_save, sender=CustomerRequestDeposit)
def create_customer_request(sender, created, instance, **kwargs):
    title = f"New customer request from {instance.customer_phone}"
    transaction_type = "Customer"
    message = f"{instance.customer_phone} just made a request of {instance.amount}"

    if created:
        Notifications.objects.create(user=instance.agent, transaction_type=transaction_type, item_id=instance.id,
                                     notification_title=title, notification_message=message,
                                     customer=instance.customer_phone, user2=instance.agent,
                                     customer_request_slug=instance.slug)


@receiver(post_save, sender=ExpensesRequest)
def create_expense_request(sender, created, instance, **kwargs):
    title = f"New Expense Request from {instance.agent.username}"
    message = f"{instance.agent.username} just made an expense request of {instance.amount}"
    transaction_type = "Cash"

    if created:
        Notifications.objects.create(user=instance.agent, item_id=instance.id, transaction_type=transaction_type,
                                     notification_title=title, notification_message=message, user2=instance.guarantor, )


@receiver(post_save, sender=BankDeposit)
def create_bank_request(sender, created, instance, **kwargs):
    title = f"New Bank Deposit from {instance.agent.username}"
    message = f"{instance.agent.username} just made a bank deposit of {instance.amount}"
    transaction_type = "Bank"

    if created:
        Notifications.objects.create(user=instance.agent, item_id=instance.id, transaction_type=transaction_type,
                                     notification_title=title, notification_message=message,
                                     user2=instance.guarantor, cash_deposit_request_slug=instance.slug,
                                     notification_to_customer=instance.customer)


@receiver(post_save, sender=MyPayments)
def create_payment(sender, created, instance, **kwargs):
    title = f"New payment from {instance.agent.username}"
    message = f"{instance.agent.username} just made a payment amount of {instance.amount}"
    admin_user = User.objects.get(id=1)
    transaction_type = "Payment"

    if created:
        Notifications.objects.create(user=instance.agent, item_id=instance.id, transaction_type=transaction_type,
                                     notification_title=title, notification_message=message,
                                     user2=admin_user, payment_slug=instance.slug)


@receiver(post_save, sender=OTP)
def send_otp_to_customer_admin(sender, created, instance, **kwargs):
    title = f"OTP for verification"
    message = f"Your code to confirm deposit with {instance.agent.username} is {instance.otp}"
    transaction_type = "OTP"

    if created:
        Notifications.objects.create(user=instance.agent, item_id=instance.id, transaction_type=transaction_type,
                                     notification_title=title, notification_message=message,
                                     notification_from=instance.agent,
                                     notification_to_guarantor=instance.guarantor, user2=instance.guarantor,
                                     notification_to_customer=instance.customer)


@receiver(post_save, sender=CustomerPaymentAtBank)
def send_otp_to_customer_admin(sender, created, instance, **kwargs):
    title = f"Bank Payment from Customer"
    message = f"{instance.customer} has made a bank payment of {instance.amount}"
    transaction_type = "Customer Bank Payment"

    if created:
        Notifications.objects.create(item_id=instance.id, transaction_type=transaction_type,
                                     notification_title=title, notification_message=message,
                                     notification_from=instance.customer, user2=instance.guarantor,
                                     )
