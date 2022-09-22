from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomerRequestDeposit, ExpensesRequest, BankDeposit, MyPayments, Notifications, OTP, \
    CustomerPaymentAtBank, Customer, AddedToApprovedDeposits, AddedToApprovedPayment, Reports, GroupMessage, \
    PrivateUserMessage
from django.conf import settings

User = settings.AUTH_USER_MODEL
from users.models import User


@receiver(post_save, sender=AddedToApprovedPayment)
def alert_payment_approved(sender, created, instance, **kwargs):
    title = "Payment approved"
    transaction_type = "Payment Approved"
    message = f"Your payment of {instance.payment.amount} was approved successfully."

    if created:
        Notifications.objects.create(user=instance.payment.agent, transaction_type=transaction_type,
                                     item_id=instance.id,
                                     notification_title=title, notification_message=message,
                                     user2=instance.payment.agent,
                                     )


@receiver(post_save, sender=AddedToApprovedDeposits)
def alert_bank_deposit_approved(sender, created, instance, **kwargs):
    title = "Bank Deposit approved"
    transaction_type = "Bank Deposit Approved"
    message = f"Your bank deposit of {instance.bank_deposit.amount} was approved successfully."

    if created:
        Notifications.objects.create(user=instance.bank_deposit.agent, transaction_type=transaction_type,
                                     item_id=instance.id,
                                     notification_title=title, notification_message=message,
                                     user2=instance.bank_deposit.agent,
                                     notification_to_customer=instance.bank_deposit.customer
                                     )


@receiver(post_save, sender=Customer)
def alert_customer_created(sender, created, instance, **kwargs):
    title = "A new customer was added to the system"
    transaction_type = "Customer Created"
    message = f"A customer with the name of {instance.name} was added to the system"

    if created:
        Notifications.objects.create(user=instance.agent, transaction_type=transaction_type, item_id=instance.id,
                                     notification_title=title, notification_message=message,
                                     customer=instance.customer_phone, user2=instance.agent,
                                     notification_to_admin=instance.administrator,
                                     notification_to_customer=instance.customer
                                     )


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
    message = f"{instance.agent.username} just made a bank deposit of {instance.amount} for {instance.customer}"
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
    admin_user = User.objects.get(id=1)

    if created:
        Notifications.objects.create(item_id=instance.id, transaction_type=transaction_type,
                                     notification_title=title, notification_message=message,
                                     notification_from_customer=instance.customer, user2=admin_user,
                                     )


@receiver(post_save, sender=Reports)
def alert_report(sender, created, instance, **kwargs):
    title = f"New Report"
    message = f"{instance.user.username} submitted a new report"
    transaction_type = "New Report"

    if created:
        Notifications.objects.create(item_id=instance.id, transaction_type=transaction_type,
                                     notification_title=title, notification_message=message,
                                     notification_from_customer=instance.user, user2=instance.administrator,
                                     )


@receiver(post_save, sender=GroupMessage)
def alert_pub_message(sender, created, instance, **kwargs):
    title = f"New group message"
    message = f"{instance.user.username} sent a message to the group"
    transaction_type = "New group message"

    users = User.objects.exclude(id=instance.user.id)

    if created:
        for i in users:
            Notifications.objects.create(item_id=instance.id, transaction_type=transaction_type,
                                         notification_title=title, notification_message=message,
                                         notification_from=instance.user, user2=i,
                                         )


@receiver(post_save, sender=PrivateUserMessage)
def alert_private_message(sender, created, instance, **kwargs):
    title = f"New private message"
    transaction_type = "New private message"

    if created:
        if instance.sender:
            message = f"{instance.sender.username} sent you a message"
            Notifications.objects.create(item_id=instance.id, notification_title=title,
                                         notification_message=message, transaction_type=transaction_type,
                                         notification_to=instance.receiver)
        if instance.receiver:
            message = f"{instance.receiver.username} sent you a message"
            Notifications.objects.create(item_id=instance.id, notification_title=title,
                                         notification_message=message, transaction_type=transaction_type,
                                         notification_to=instance.sender)
