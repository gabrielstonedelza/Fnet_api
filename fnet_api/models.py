from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from django.utils.text import slugify

import datetime

User = settings.AUTH_USER_MODEL
ID_TYPES = (
    ("Select Id Type", "Select Id Type"),
    ("Ghana Card", "Ghana Card"),
    ("Passport", "Passport"),
    ("Drivers License", "Drivers License"),
    ("Voters Id", "Voters Id"),
    ("Cheque", "Cheque"),
    ("Atm Phone", "Atm Phone"),
)
BANKS = (
    ("Select bank", "Select bank"),
    ("Access Bank", "Access Bank"),
    ("Cal Bank", "Cal Bank"),
    ("Fidelity Bank", "Fidelity Bank"),
    ("Ecobank", "Ecobank"),
    ("Pan Africa", "Pan Africa"),
    ("First Bank of Nigeria", "First Bank of Nigeria"),
    ("SGSSB", "SGSSB"),
    ("Atwima Rural Bank", "Atwima Rural Bank"),
    ("Omnibsic Bank", "Omnibsic Bank"),
    ("Stanbic Bank", "Stanbic Bank"),
    ("Absa Bank", "Absa Bank"),
    ("Universal Merchant Bank", "Universal Merchant Bank"),
)
PAYMENT_ACTIONS = (
    ("Select payment action", "Select payment action"),
    ("Not Closed", "Not Closed"),
    ("Close Payment", "Close Payment"),
)

NETWORKS = (
    ("Select Network", "Select Network"),
    ("Mtn", "Mtn"),
    ("AirtelTigo", "AirtelTigo"),
    ("Vodafone", "Vodafone"),
)

DEPOSIT_REQUEST_OPTIONS = (
    ("Cash", "Cash"),
    ("Mobile Money", "Money Money"),
    ("Bank", "Bank"),
)

MOBILE_MONEY_DEPOSIT_TYPE = (
    ("Regular", "Regular"),
    ("Direct", "Direct"),
    ("Agent to Agent", "Agent to Agent"),
)
MOBILE_MONEY_ACTION = (
    ("Deposit", "Deposit"),
    ("Withdraw", "Withdraw"),
)

WITHDRAW_TYPES = (
    ("MomoPay", "MomoPay"),
    ("Cash Out", "Cash Out"),
    ("Agent to Agent", "Agent to Agent"),
)

REQUEST_STATUS = (
    ("Approved", "Approved"),
    ("Pending", "Pending")
)

MODE_OF_PAYMENT = (
    ("Select mode of payment", "Select mode of payment"),
    ("Bank Payment", "Bank Payment"),
    ("Mtn", "Mtn"),
    ("AirtelTigo", "AirtelTigo"),
    ("Vodafone", "Vodafone"),
    ("Momo pay", "Momo pay"),
    ("Agent to Agent", "Agent to Agent"),
    ("Cash left @", "Cash left @"),
    ("Own Accounts", "Own Accounts"),
    ("Company Accounts", "Company Accounts"),
)

PAYMENT_OFFICES = (
    ("Please select cash at location", "Please select cash at location"),
    ("Cash @ location", "Cash @ location"),
    ("DVLA", "DVLA"),
    ("HEAD OFFICE", "HEAD OFFICE"),
    ("KEJETIA", "KEJETIA"),
    ("ECOBANK", "ECOBANK"),
    ("PAN AFRICA", "PAN AFRICA"),
)

REQUEST_PAID_OPTIONS = (
    ("Not Paid", "Not Paid"),
    ("Paid", "Paid"),
)

NOTIFICATIONS_STATUS = (
    ("Read", "Read"),
    ("Not Read", "Not Read"),
)

NOTIFICATIONS_TRIGGERS = (
    ("Triggered", "Triggered"),
    ("Not Triggered", "Not Triggered"),
)


class CustomerRequestDeposit(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    customer_phone = models.CharField(max_length=20, blank=True)
    customer_name = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2, blank=True)
    request_option = models.CharField(max_length=100, choices=DEPOSIT_REQUEST_OPTIONS, default="Physical Cash")
    request_status = models.CharField(max_length=20, choices=REQUEST_STATUS, default="Pending")
    date_requested = models.DateField(auto_now_add=True)
    time_requested = models.TimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, allow_unicode=True, default='')

    def __str__(self):
        return self.customer_name

    def save(self, *args, **kwargs):
        value = self.customer_name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class WithdrawReference(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    customer_phone = models.CharField(max_length=20)
    reference_id = models.CharField(max_length=50)
    date_withdrew = models.DateField(auto_now_add=True)
    time_withdrew = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.reference_id


class CashAtPayments(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    left_with = models.CharField(max_length=50)
    left_with_phone = models.CharField(max_length=20)
    reference_id = models.CharField(max_length=50)
    date_paid = models.DateField(auto_now_add=True)
    time_paid = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.agent.username


class Customer(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=True)
    location = models.CharField(max_length=100, blank=True)
    digital_address = models.CharField(max_length=25, blank=True)
    id_type = models.CharField(max_length=50, choices=ID_TYPES, blank=True, default="Passport")
    id_number = models.CharField(max_length=50, blank=True, default="")
    phone = models.CharField(max_length=15, unique=True, blank=True)
    date_of_birth = models.CharField(max_length=15, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CustomerAccounts(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=16)
    account_name = models.CharField(max_length=100)
    bank = models.CharField(max_length=100, choices=BANKS, default="Access Bank")
    phone = models.CharField(max_length=15)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone


class ExpensesRequest(models.Model):
    guarantor = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agent_requesting_expense_cash")
    amount = models.DecimalField(max_digits=19, decimal_places=2, blank=True)
    reason = models.TextField(default="")
    request_status = models.CharField(max_length=20, choices=REQUEST_STATUS, default="Pending")
    deposit_paid = models.CharField(choices=REQUEST_PAID_OPTIONS, default="Not Paid", blank=True, max_length=20)
    date_requested = models.DateField(auto_now_add=True)
    time_requested = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"Expense request made for {self.amount} by {self.agent.username}"


class BankDeposit(models.Model):
    guarantor = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    customer = models.CharField(max_length=20, blank=True)
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agent_requesting_bank")
    bank = models.CharField(max_length=50, choices=BANKS, blank=True, default="")
    account_number = models.TextField(blank=True, max_length=17)
    account_name = models.CharField(max_length=100, blank=True, default="")
    amount = models.DecimalField(max_digits=19, decimal_places=2, blank=True)
    depositor_name = models.CharField(max_length=50, blank=True, default="")
    request_status = models.CharField(max_length=20, choices=REQUEST_STATUS, default="Pending")
    deposit_paid = models.CharField(choices=REQUEST_PAID_OPTIONS, default="Not Paid", blank=True, max_length=20)
    date_requested = models.DateField(auto_now_add=True)
    time_requested = models.TimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, default='')

    def __str__(self):
        return f"Bank request made for {self.amount} by {self.agent.username}"

    def save(self, *args, **kwargs):
        value = self.customer
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class MobileMoneyDeposit(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agent_requesting")
    customer_phone = models.CharField(max_length=30, blank=True)
    customer_name = models.CharField(max_length=30, blank=True)
    depositor_name = models.CharField(max_length=30, blank=True,default="")
    depositor_number = models.CharField(max_length=30, blank=True,default="")
    network = models.CharField(max_length=20, choices=NETWORKS, blank=True, default="Select Network")
    type = models.CharField(max_length=20, blank=True, choices=MOBILE_MONEY_DEPOSIT_TYPE)
    amount = models.DecimalField(max_digits=19, decimal_places=2, blank=True)
    charges = models.DecimalField(max_digits=19, decimal_places=2, default=0.0)
    agent_commission = models.DecimalField(max_digits=19, decimal_places=2, default=0.0)
    date_deposited = models.DateField(auto_now_add=True)
    time_deposited = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"Mobile money request made for {self.amount}"


class MobileMoneyWithdraw(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_phone = models.CharField(max_length=30, blank=True)
    customer_name = models.CharField(max_length=30, blank=True)
    network = models.CharField(max_length=20, choices=NETWORKS, blank=True, default="Select Network")
    type = models.CharField(max_length=30, choices=WITHDRAW_TYPES, blank=True, default="")
    id_type = models.CharField(max_length=30, choices=ID_TYPES)
    id_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=19, decimal_places=2, blank=True)
    charges = models.DecimalField(max_digits=19, decimal_places=2, default=0.0)
    cash_out_commission = models.DecimalField(max_digits=19, decimal_places=2, default=0.0)
    agent_commission = models.DecimalField(max_digits=19, decimal_places=2, default=0.0)
    mtn_commission = models.DecimalField(max_digits=19, decimal_places=2, default=0.0)
    date_of_withdrawal = models.DateField(auto_now_add=True)
    time_of_withdrawal = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"Withdrawal made for {self.amount}"


class UserMobileMoneyAccountsStarted(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    physical = models.DecimalField(max_digits=19, decimal_places=2)
    mtn_ecash = models.DecimalField(max_digits=19, decimal_places=2)
    tigoairtel_ecash = models.DecimalField(max_digits=19, decimal_places=2)
    vodafone_ecash = models.DecimalField(max_digits=19, decimal_places=2)
    ecash_total = models.DecimalField(max_digits=19, decimal_places=2, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.agent.username

    def save(self, *args, **kwargs):
        e_total = self.mtn_ecash + self.tigoairtel_ecash + self.vodafone_ecash

        self.ecash_total = e_total
        super().save(*args, **kwargs)


class UserMobileMoneyAccountsClosed(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    physical = models.DecimalField(max_digits=19, decimal_places=2)
    mtn_ecash = models.DecimalField(max_digits=19, decimal_places=2)
    tigoairtel_ecash = models.DecimalField(max_digits=19, decimal_places=2)
    vodafone_ecash = models.DecimalField(max_digits=19, decimal_places=2)
    ecash_total = models.DecimalField(max_digits=19, decimal_places=2, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.agent.username

    def save(self, *args, **kwargs):
        e_total = self.mtn_ecash + self.tigoairtel_ecash + self.vodafone_ecash
        self.ecash_total = e_total
        super().save(*args, **kwargs)


class CustomerWithdrawal(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.CharField(max_length=100)
    bank = models.CharField(max_length=100, choices=BANKS, default="GT Bank")
    id_type = models.CharField(max_length=20, choices=ID_TYPES)
    id_number = models.CharField(max_length=20,default="0")
    amount = models.DecimalField(max_digits=19, decimal_places=2)

    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Withdrawal made for {self.amount} by {self.agent.username}"


class MyPayments(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    mode_of_payment1 = models.CharField(max_length=30, choices=MODE_OF_PAYMENT, blank=True)
    mode_of_payment2 = models.CharField(max_length=30, choices=MODE_OF_PAYMENT, blank=True)
    cash_at_location1 = models.CharField(max_length=30, choices=PAYMENT_OFFICES, blank=True, default="")
    cash_at_location2 = models.CharField(max_length=30, choices=PAYMENT_OFFICES, blank=True, default="")
    bank1 = models.CharField(max_length=50, choices=BANKS, blank=True)
    bank2 = models.CharField(max_length=50, choices=BANKS, blank=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2, default=0.0, blank=True)
    amount1 = models.DecimalField(max_digits=19, decimal_places=2, default=0.0)
    amount2 = models.DecimalField(max_digits=19, decimal_places=2, default=0.0)
    transaction_id1 = models.CharField(max_length=30, blank=True, default="")
    transaction_id2 = models.CharField(max_length=30, blank=True, default="")
    payment_action = models.CharField(max_length=50, choices=PAYMENT_ACTIONS, default="Close Payment")
    payment_status = models.CharField(max_length=20, choices=REQUEST_STATUS, default="Pending")
    date_created = models.DateField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, default='')

    def __str__(self):
        if self.payment_status == "Pending":
            return f"{self.agent.username}'s payment is pending"
        return f"{self.agent.username}'s payment is approved"

    def save(self, *args, **kwargs):
        value = self.mode_of_payment1
        self.slug = slugify(value, allow_unicode=True)

        amount_total = Decimal(self.amount1) + Decimal(self.amount2)
        self.amount = Decimal(amount_total)
        super().save(*args, **kwargs)


class AdminAccountsStartedWith(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    physical_cash = models.DecimalField(max_digits=19, decimal_places=2)
    eCash = models.DecimalField(max_digits=19, decimal_places=2)
    date_started = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} has started accounts today"


class AdminAccountsCompletedWith(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    physical_cash = models.DecimalField(max_digits=19, decimal_places=2)
    eCash = models.DecimalField(max_digits=19, decimal_places=2)
    date_closed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} has ended accounts today"


class Notifications(models.Model):
    item_id = models.CharField(max_length=100, blank=True, default="")
    transaction_type = models.CharField(max_length=100, blank=True, default="")
    notification_title = models.CharField(max_length=200, blank=True)
    notification_message = models.TextField(blank=True)
    read = models.CharField(max_length=20, choices=NOTIFICATIONS_STATUS, default="Not Read")
    notification_trigger = models.CharField(max_length=100, choices=NOTIFICATIONS_TRIGGERS, default="Triggered",
                                            blank=True)
    customer = models.CharField(max_length=100, blank=True, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User_receiving_notification", null=True)
    customer_request_slug = models.CharField(max_length=100, blank=True)
    cash_deposit_request_slug = models.CharField(max_length=100, blank=True)
    bank_deposit_request_slug = models.CharField(max_length=100, blank=True)
    payment_slug = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, default='')

    def __str__(self):
        return self.notification_title

    def save(self, *args, **kwargs):
        value = self.notification_title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
