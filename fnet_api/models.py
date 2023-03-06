from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import random
from datetime import datetime, date, time
from django.shortcuts import get_object_or_404
from django.contrib.humanize.templatetags import humanize

User = settings.AUTH_USER_MODEL
ID_TYPES = (
    ("Select Id Type", "Select Id Type"),
    ("Ghana Card", "Ghana Card"),
    ("Passport", "Passport"),
    ("Drivers License", "Drivers License"),
    ("Voters Id", "Voters Id"),
)
BANK_REDRAW_ID_TYPES = (
    ("Select Withdrawal Type", "Select Withdrawal Type"),
    ("Cheque", "Cheque"),
    ("Atm", "Atm"),
    ("Phone", "Phone"),
)
BANKS = (
    ("Select bank", "Select bank"),
    ("Access Bank", "Access Bank"),
    ("Cal Bank", "Cal Bank"),
    ("Fidelity Bank", "Fidelity Bank"),
    ("Ecobank", "Ecobank"),
    ("Adansi rural bank", "Adansi rural bank"),
    ("Kwumawuman Bank", "Kwumawuman Bank"),
    ("Pan Africa", "Pan Africa"),
    ("SGSSB", "SGSSB"),
    ("Atwima Rural Bank", "Atwima Rural Bank"),
    ("Omnibsic Bank", "Omnibsic Bank"),
    ("Omini bank", "Omini bank"),
    ("Stanbic Bank", "Stanbic Bank"),
    ("First Bank of Nigeria", "First Bank of Nigeria"),
    ("Adehyeman Savings and loans", "Adehyeman Savings and loans",),
    ("ARB Apex Bank Limited", "ARB Apex Bank Limited",),
    ("Absa Bank", "Absa Bank"),
    ("Agriculture Development bank", "Agriculture Development bank"),
    ("Bank of Africa", "Bank of Africa"),
    ("Bank of Ghana", "Bank of Ghana"),
    ("Consolidated Bank Ghana", "Consolidated Bank Ghana"),
    ("First Atlantic Bank", "First Atlantic Bank"),
    ("First National Bank", "First National Bank"),
    ("G-Money", "G-Money"),
    ("GCB BanK LTD", "GCB BanK LTD"),
    ("Ghana Pay", "Ghana Pay"),
    ("GHL Bank Ltd", "GHL Bank Ltd"),
    ("GT Bank", "GT Bank"),
    ("National Investment Bank", "National Investment Bank"),
    ("Opportunity International Savings And Loans", "Opportunity International Savings And Loans"),
    ("Prudential Bank", "Prudential Bank"),
    ("Republic Bank Ltd", "Republic Bank Ltd"),
    ("Sahel Sahara Bank", "Sahel Sahara Bank"),
    ("Sinapi Aba Savings and Loans", "Sinapi Aba Savings and Loans"),
    ("Societe Generale Ghana Ltd", "Societe Generale Ghana Ltd"),
    ("Standard Chartered", "Standard Chartered"),
    ("universal Merchant Bank", "universal Merchant Bank"),
    ("Zenith Bank", "Zenith Bank"),
    ("Mtn", "Mtn"),
    ("AirtelTigo", "AirtelTigo"),
    ("Vodafone", "Vodafone"),
)

PAYMENT_ACTIONS = (
    ("Select payment action", "Select payment action"),
    ("Not Closed", "Not Closed"),
    ("Close Payment", "Close Payment"),
)

NETWORKS = (
    ("Select Network", "Select Network"),
    ("Mtn", "Mtn"),
    ("Tigo", "Tigo"),
    ("AirtelTigo", "AirtelTigo"),
    ("Vodafone", "Vodafone"),
)

DEPOSIT_REQUEST_OPTIONS = (
    ("Cash", "Cash"),
    ("Mobile Money", "Money Money"),
    ("Bank", "Bank"),
)

MOBILE_MONEY_DEPOSIT_TYPE = (
    ("Loading", "Loading"),
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
    ("MELCOM SANTASI", "MELCOM SANTASI"),
    ("MELCOM TANOSO", "MELCOM TANOSO"),
    ("MELCOM MANHYIA", "MELCOM MANHYIA"),
    ("MELCOM TAFO", "MELCOM TAFO"),
    ("MELCOM AHODWO", "MELCOM AHODWO"),
    ("MELCOM ADUM", "MELCOM ADUM"),
    ("MELCOM SUAME", "MELCOM SUAME"),
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

REDEEM_POINTS_OPTIONS = (
    ("Select Option", "Select Option"),
    ("Express Accounts", "Express Accounts"),
    ("Airtime", "Airtime"),
    ("Melcom Coupon", "Melcom Coupon"),
)

CUSTOMER_REFERRAL_STATUS = (
    ("Was Referred", "Was Referred"),
    ("User Registration", "User Registration"),
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
    administrator = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name="de_administrator")
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=True)
    location = models.CharField(max_length=100, blank=True)
    digital_address = models.CharField(max_length=25, blank=True)
    id_type = models.CharField(max_length=50, choices=ID_TYPES, blank=True, default="Passport")
    id_number = models.CharField(max_length=50, blank=True, default="")
    phone = models.CharField(max_length=15, unique=True, blank=True)
    points = models.DecimalField(max_digits=19, decimal_places=2, blank=True, default="0.0")
    referral = models.CharField(max_length=200, blank=True, default="")
    status = models.CharField(max_length=100, choices=CUSTOMER_REFERRAL_STATUS, default="User Registration", blank=True)
    date_of_birth = models.CharField(max_length=15, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_agents_phone(self):
        return self.agent.phone


class ReferCustomer(models.Model):
    administrator = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name="referral_administrator")
    name = models.CharField(max_length=150, blank=True, unique=True)
    location = models.CharField(max_length=100, blank=True)
    digital_address = models.CharField(max_length=25, blank=True)
    id_type = models.CharField(max_length=50, choices=ID_TYPES, blank=True, default="Passport")
    id_number = models.CharField(max_length=50, blank=True, default="")
    phone = models.CharField(max_length=15, unique=True, blank=True, )
    referral = models.CharField(max_length=200, blank=True, default="")
    status = models.CharField(max_length=100, choices=CUSTOMER_REFERRAL_STATUS, default="Was Referred", blank=True)
    created = models.BooleanField(default=False)
    date_of_birth = models.CharField(max_length=15, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AddToCustomerPoints(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer_phone = models.CharField(max_length=20, blank=True)
    points = models.DecimalField(max_digits=19, decimal_places=2, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        c_points = str(self.points)
        return f"{self.customer.name} has {c_points} points"


class AddToCustomerRedeemPoints(models.Model):
    administrator = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer_phone = models.CharField(max_length=20, blank=True)
    points = models.DecimalField(max_digits=19, decimal_places=2, blank=True)
    redeem_option = models.CharField(max_length=100, choices=REDEEM_POINTS_OPTIONS, default="Airtime")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        c_points = str(self.points)
        return f"{self.customer.name} has redeemed {c_points} points"

    def get_customer_name(self):
        return self.customer.name

    def get_customer_phone(self):
        return self.customer.phone


class CustomerAccounts(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=16, blank=True)
    account_name = models.CharField(max_length=100, blank=True)
    bank = models.CharField(max_length=100, choices=BANKS, default="Access Bank")
    phone = models.CharField(max_length=15, blank=True)
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
    deposited_month = models.CharField(max_length=10, blank=True, default="")
    deposited_year = models.CharField(max_length=10, blank=True, default="")
    time_requested = models.TimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, default='')

    def __str__(self):
        if self.request_status == "Pending":
            return f"{self.agent.username}'s deposit is pending"
        return f"{self.agent.username}'s deposit is approved, '{self.deposit_paid}'"

    def save(self, *args, **kwargs):
        my_date = datetime.today()
        de_date = my_date.date()
        self.deposited_month = de_date.month
        self.deposited_year = de_date.year
        value = self.customer
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class AddedToApprovedDeposits(models.Model):
    bank_deposit = models.ForeignKey(BankDeposit, on_delete=models.CASCADE)
    date_approved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ghs {self.bank_deposit.amount} was approved for {self.bank_deposit.agent.username}"


class MobileMoneyDeposit(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agent_requesting")
    customer_phone = models.CharField(max_length=30, blank=True)
    # customer_name = models.CharField(max_length=30, blank=True)
    depositor_name = models.CharField(max_length=30, blank=True, default="")
    depositor_number = models.CharField(max_length=30, blank=True, default="")
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
    # customer_name = models.CharField(max_length=30, blank=True)
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
    withdrawal_type = models.CharField(max_length=120, choices=BANK_REDRAW_ID_TYPES, default="Cheque")
    id_type = models.CharField(max_length=20, choices=ID_TYPES)
    id_number = models.CharField(max_length=20, default="0")
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
    payment_month = models.CharField(max_length=10, blank=True, default="")
    payment_year = models.CharField(max_length=10, blank=True, default="")
    date_created = models.DateField(auto_now_add=True)
    time_created = models.TimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, default='')

    def __str__(self):
        if self.payment_status == "Pending":
            return f"{self.agent.username}'s payment is pending"
        return f"{self.agent.username}'s payment is approved"

    def save(self, *args, **kwargs):
        my_date = datetime.today()
        de_date = my_date.date()
        self.payment_month = de_date.month
        self.payment_year = de_date.year
        value = self.mode_of_payment1
        self.slug = slugify(value, allow_unicode=True)

        amount_total = Decimal(self.amount1) + Decimal(self.amount2)
        self.amount = Decimal(amount_total)
        super().save(*args, **kwargs)


class AddedToApprovedPayment(models.Model):
    payment = models.ForeignKey(MyPayments, on_delete=models.CASCADE)
    date_approved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment.amount} was approved"


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
    notification_to_admin = models.ForeignKey(User, on_delete=models.CASCADE,
                                              related_name="administrator_notifications", default=1)
    customer_request_slug = models.CharField(max_length=100, blank=True)
    cash_deposit_request_slug = models.CharField(max_length=100, blank=True)
    bank_deposit_request_slug = models.CharField(max_length=100, blank=True)
    payment_slug = models.CharField(max_length=100, blank=True)
    notification_from = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                                          related_name="user_sending_notification")
    notification_to_guarantor = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True,
                                                  related_name="guarantor_notification")
    notification_to_customer = models.CharField(max_length=100, blank=True, default="")
    notification_from_customer = models.CharField(max_length=100, blank=True, default="")
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, default='')

    def __str__(self):
        return self.notification_title

    def save(self, *args, **kwargs):
        value = self.notification_title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class PaymentAtBank(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    teller_name = models.CharField(max_length=100)
    teller_phone = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=19, default=0.0)
    total = models.DecimalField(decimal_places=2, max_digits=19, default=0.0)
    d_200 = models.IntegerField(default=0, blank=True)
    d_100 = models.IntegerField(default=0, blank=True)
    d_50 = models.IntegerField(default=0, blank=True)
    d_20 = models.IntegerField(default=0, blank=True)
    d_10 = models.IntegerField(default=0, blank=True)
    d_5 = models.IntegerField(default=0, blank=True)
    d_2 = models.IntegerField(default=0, blank=True)
    d_1 = models.IntegerField(default=0, blank=True)
    date_added = models.DateField(auto_now_add=True)
    time_added = models.TimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        two_h_cedis_values = self.d_200 * 200
        one_h_cedis_values = self.d_100 * 100
        fifty_cedis_values = self.d_50 * 50
        twenty_cedis_values = self.d_20 * 20
        ten_cedis_values = self.d_10 * 10
        five_cedis_values = self.d_5 * 5
        two_cedis_values = self.d_2 * 2
        one_cedi_values = self.d_1 * 1

        amount_total = Decimal(two_h_cedis_values) + Decimal(one_h_cedis_values) + Decimal(
            fifty_cedis_values) + Decimal(
            twenty_cedis_values) + Decimal(ten_cedis_values) + Decimal(five_cedis_values) + Decimal(
            two_cedis_values) + Decimal(one_cedi_values)
        self.total = Decimal(amount_total)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.total)


class OTP(models.Model):
    guarantor = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    customer = models.CharField(max_length=20, blank=True)
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agent_depositing")
    otp = models.CharField(max_length=10)
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer


class CustomerPaymentAtBank(models.Model):
    customer = models.CharField(max_length=100)
    agent_name = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=19, default=0.0)
    total = models.DecimalField(decimal_places=2, max_digits=19, default=0.0)
    d_200 = models.IntegerField(default=0, blank=True)
    d_100 = models.IntegerField(default=0, blank=True)
    d_50 = models.IntegerField(default=0, blank=True)
    d_20 = models.IntegerField(default=0, blank=True)
    d_10 = models.IntegerField(default=0, blank=True)
    d_5 = models.IntegerField(default=0, blank=True)
    d_2 = models.IntegerField(default=0, blank=True)
    d_1 = models.IntegerField(default=0, blank=True)
    date_added = models.DateField(auto_now_add=True)
    time_added = models.TimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        two_h_cedis_values = self.d_200 * 200
        one_h_cedis_values = self.d_100 * 100
        fifty_cedis_values = self.d_50 * 50
        twenty_cedis_values = self.d_20 * 20
        ten_cedis_values = self.d_10 * 10
        five_cedis_values = self.d_5 * 5
        two_cedis_values = self.d_2 * 2
        one_cedi_values = self.d_1 * 1

        amount_total = Decimal(two_h_cedis_values) + Decimal(one_h_cedis_values) + Decimal(
            fifty_cedis_values) + Decimal(
            twenty_cedis_values) + Decimal(ten_cedis_values) + Decimal(five_cedis_values) + Decimal(
            two_cedis_values) + Decimal(one_cedi_values)
        self.total = Decimal(amount_total)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.total)


class Reports(models.Model):
    administrator = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name="admin_user")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.TextField()
    read = models.BooleanField(default=False)
    date_reported = models.DateField(auto_now_add=True)
    time_reported = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def get_username(self):
        return self.user.username


# messages
class FnetGroupMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

    def get_username(self):
        return self.user.username

    def get_phone_number(self):
        return self.user.phone

    def get_date(self):
        return humanize.naturaltime(self.timestamp)


class PrivateChatId(models.Model):
    chat_id = models.CharField(max_length=400, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.chat_id


class FnetPrivateUserMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chatter2")
    private_chat_id = models.CharField(max_length=400, blank=True)
    message = models.TextField()
    read = models.BooleanField(default=False)
    isSender = models.BooleanField(default=False)
    isReceiver = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.private_chat_id

    def get_senders_username(self):
        return self.sender.username

    def get_receivers_username(self):
        return self.receiver.username

    def get_date(self):
        return humanize.naturaltime(self.timestamp)

    def save(self, *args, **kwargs):
        senders_username = self.sender.username
        receiver_username = self.receiver.username
        sender_receiver = str(senders_username) + str(receiver_username)
        receiver_sender = str(receiver_username) + str(senders_username)

        self.private_chat_id = sender_receiver

        super().save(*args, **kwargs)


class AddToBlockList(models.Model):
    administrator = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_being_blocked")
    date_blocked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def get_username(self):
        return self.user.username


class CashRequest(models.Model):
    administrator = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    agent1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agent_requesting_cash")
    agent2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agent_delivering_cash")
    amount = models.DecimalField(max_digits=19, decimal_places=2, blank=True)
    request_status = models.CharField(max_length=20, choices=REQUEST_STATUS, default="Pending")
    date_requested = models.DateField(auto_now_add=True)
    requested_month = models.CharField(max_length=10, blank=True, default="")
    requested_year = models.CharField(max_length=10, blank=True, default="")
    time_requested = models.TimeField(auto_now_add=True)

    def get_agent1_username(self):
        return self.agent1.username

    def get_agent2_username(self):
        return self.agent2.username

    def __str__(self):
        if self.request_status == "Pending":
            return f"{self.agent1.username}'s cash deposit is pending"
        return f"{self.agent1.username}'s cash deposit is approved"

    def save(self, *args, **kwargs):
        my_date = datetime.today()
        de_date = my_date.date()
        self.requested_month = de_date.month
        self.requested_year = de_date.year
        super().save(*args, **kwargs)