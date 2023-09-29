from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (CustomerRequestDeposit, ExpensesRequest, BankDeposit, MyPayments, Notifications, OTP, \
                     CustomerPaymentAtBank, Customer, AddedToApprovedDeposits, AddedToApprovedPayment, Reports,
                     FnetGroupMessage, CashRequest,MyCashPayments,AddedToApprovedCashPayment,
                     FnetPrivateUserMessage, AddToCustomerPoints, AddToCustomerRedeemPoints, ReferCustomer)
from django.conf import settings

User = settings.AUTH_USER_MODEL
from users.models import User

# new signals with websocket client
# @receiver(post_save, sender=BankDeposit)
# def send_new_post_notification(sender, instance, **kwargs):
#     from channels.layers import get_channel_layer
#     import json
#
#     channel_layer = get_channel_layer()
#     bank_deposit_data = {
#         'id': instance.id,
#         'title': "New bank deposit",
#         # Include other post data fields as needed
#     }
#
#     # Send a notification to the WebSocket consumer
#     async_to_sync(channel_layer.group_send)(
#         'bank_deposit_group',
#         {
#             'type': 'new_post_notification',
#             'bank_deposit_data': bank_deposit_data,
#         }
#     )

@receiver(post_save,sender=CashRequest)
def alert_cash_request(sender,created,instance,**kwargs):
    title = "New Cash Request"
    message1 = f"{instance.agent1.username} is requesting cash worth of {instance.amount} from you."
    message2 = f"{instance.agent1.username} is requesting cash worth of {instance.amount} from  {instance.agent2.username}."
    transaction_type = "Cash Request"

    if created:
        Notifications.objects.create(user=instance.agent1, transaction_type=transaction_type,
                                     item_id=instance.id,
                                     notification_title=title, notification_message=message1,
                                     user2=instance.agent2,
                                     )

        Notifications.objects.create(user=instance.agent1, transaction_type=transaction_type,
                                     item_id=instance.id,
                                     notification_title=title, notification_message=message2,
                                     user2=instance.administrator,
                                     )


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

@receiver(post_save, sender=AddedToApprovedCashPayment)
def alert_cash_payment_approved(sender, created, instance, **kwargs):
    title = "Payment approved"
    transaction_type = "Payment Approved"
    message = f"Your cash payment of {instance.payment.amount} was approved successfully."

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
                                     customer=instance.phone, user2=instance.agent,
                                     notification_to_admin=instance.administrator,

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
    message = f"{instance.agent.username} just made {instance.bank} deposit of {instance.amount} for {instance.customer}"
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


@receiver(post_save, sender=MyCashPayments)
def create_cash_payment(sender, created, instance, **kwargs):
    title = f"New cash payment from {instance.agent.username}"
    message = f"{instance.agent.username} just made a cash payment amount of {instance.amount}"
    admin_user = User.objects.get(id=1)
    transaction_type = "Cash Payment"

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


@receiver(post_save, sender=FnetGroupMessage)
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


@receiver(post_save, sender=FnetPrivateUserMessage)
def alert_private_message(sender, created, instance, **kwargs):
    title = f"New private message"
    transaction_type = "New private message"

    if created:
        if instance.sender:
            message = f"{instance.sender.username} sent you a message"
            Notifications.objects.create(item_id=instance.id, notification_title=title,
                                         notification_message=message, transaction_type=transaction_type,
                                         user2=instance.receiver)
        if instance.receiver:
            message = f"{instance.receiver.username} sent you a message"
            Notifications.objects.create(item_id=instance.id, notification_title=title,
                                         notification_message=message, transaction_type=transaction_type,
                                         user2=instance.sender)


# customer points
@receiver(post_save, sender=AddToCustomerPoints)
def alert_points_created(sender, created, instance, **kwargs):
    title = f"Points Updated"
    message = f"hi {instance.customer.name} your points was updated"
    transaction_type = "Points Updated"

    if created:
        Notifications.objects.create(item_id=instance.id, transaction_type=transaction_type,
                                     notification_title=title, notification_message=message,
                                     notification_to_customer=instance.customer
                                     )


@receiver(post_save, sender=AddToCustomerRedeemPoints)
def alert_points_redeemed(sender, created, instance, **kwargs):
    title = f"Points Redeemed"
    message = f"{instance.customer.name} wants to redeem his points for {instance.redeem_option}"
    transaction_type = "Points Redeemed"

    if created:
        Notifications.objects.create(item_id=instance.id, transaction_type=transaction_type,
                                     notification_title=title, notification_message=message,
                                     user2=instance.administrator
                                     )


@receiver(post_save, sender=ReferCustomer)
def alert_customer_referral(sender, created, instance, **kwargs):
    title = f"New Customer Referred"
    message = f"Got new customer referral from {instance.referral}"
    transaction_type = "New Customer Referred"

    if created:
        Notifications.objects.create(item_id=instance.id, transaction_type=transaction_type,
                                     notification_title=title, notification_message=message,
                                     user2=instance.administrator
                                     )
