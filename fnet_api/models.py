from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL
BANKS = (
    ("Access Bank", "Access Bank"),
    ("Cal Bank", "Cal Bank"),
    ("Fidelity Bank", "Fidelity Bank"),
    ("Ecobank", "Ecobank"),
    ("Pan Africa", "Pan Africa"),
    ("First Bank of Nigeria", "First Bank of Nigeria"),
    ("SGSSB", "SGSSB")
)
PAYMENT_ACTIONS = (
    ("Select payment action", "Select payment action"),
    ("Close Payment", "Close Payment"),
)

REQUEST_STATUS = (
    ("Approved", "Approved"),
    ("Pending", "Pending")
)
DEPOSIT_REQUEST_OPTIONS = (
    ("Physical Cash", "Physical Cash"),
    ("Mtn Ecash", "Mtn Ecash"),
    ("Vodafone Ecash", "Vodafone Ecash"),
    ("AirtelTigo Ecash", "AirtelTigo Ecash"),
    ("Ecobank Ecash", "Ecobank Ecash"),
    ("Calbank Ecash", "Calbank Ecash"),
    ("Fidelity Ecash", "Fidelity Ecash"),
)

MODE_OF_PAYMENT = (
    ("Select mode of payment", "Select mode of payment"),
    ("Bank Payment", "Bank Payment"),
    ("Momo Payment", "Momo Payment"),
    ("Momo pay Payment", "Momo pay Payment"),
    ("Agent to Agent", "Agent to Agent"),
    ("Cash left @", "Cash left @"),
)

PAYMENT_OFFICES = (
    ("Cash @ location", "Cash @ location"),
    ("DVLA", "DVLA"),
    ("HEAD OFFICE", "HEAD OFFICE"),
    ("KEJETIA", "KEJETIA"),
    ("ECOBANK", "ECOBANK"),
    ("PAN AFRICA", "PAN AFRICA"),
)


class Customer(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, unique=True)
    account_number = models.CharField(max_length=16)
    bank = models.CharField(max_length=100, choices=BANKS, default="Access Bank")
    location = models.CharField(max_length=100)
    digital_address = models.CharField(max_length=15)
    phone = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField(default=timezone.now)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AgentDepositRequests(models.Model):
    guarantor = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    customer = models.CharField(max_length=30, blank=True)
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agent_requesting")
    amount = models.CharField(max_length=500, blank=True)
    request_option = models.CharField(max_length=100, choices=DEPOSIT_REQUEST_OPTIONS, default="Physical Cash")
    request_status = models.CharField(max_length=20, choices=REQUEST_STATUS, default="Pending")
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request made for {self.amount}"


class CustomerWithdrawal(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.CharField(max_length=100)
    bank = models.CharField(max_length=100, choices=BANKS, default="GT Bank")
    amount = models.CharField(max_length=500)
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.amount


class Payments(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    mode_of_payment = models.CharField(max_length=30, choices=MODE_OF_PAYMENT, blank=True)
    cash_at_location = models.CharField(max_length=30, choices=PAYMENT_OFFICES, blank=True)
    bank = models.CharField(max_length=50, choices=BANKS, blank=True)
    amount = models.CharField(max_length=500, blank=True)
    reference = models.CharField(max_length=30, blank=True)
    payment_action = models.CharField(max_length=50, choices=PAYMENT_ACTIONS,default="Close Payment")
    payment_status = models.CharField(max_length=20, choices=REQUEST_STATUS, default="Pending")

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_status


class TwilioApi(models.Model):
    account_sid = models.CharField(max_length=200)
    twi_auth = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"twilio account added"


class AdminAccountsStartedWith(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    physical_cash = models.IntegerField()
    mtn_eCash = models.IntegerField()
    vodafone_eCash = models.IntegerField()
    airtel_tigo_eCash = models.IntegerField()
    ecobank_eCash = models.IntegerField()
    calbank_eCash = models.IntegerField()
    fidelity_eCash = models.IntegerField()
    date_started = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} has started accounts today"

    def ecash_sum(self):
        return self.mtn_eCash + self.vodafone_eCash + self.airtel_tigo_eCash + self.ecobank_eCash + self.calbank_eCash + self.fidelity_eCash


class AdminAccountsCompletedWith(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    physical_cash = models.IntegerField()
    mtn_eCash = models.IntegerField()
    vodafone_eCash = models.IntegerField()
    airtel_tigo_eCash = models.IntegerField()
    ecobank_eCash = models.IntegerField()
    calbank_eCash = models.IntegerField()
    fidelity_eCash = models.IntegerField()
    date_closed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} has ended accounts today"

    def ecash_sum(self):
        return self.mtn_eCash + self.vodafone_eCash + self.airtel_tigo_eCash + self.ecobank_eCash + self.calbank_eCash + self.fidelity_eCash
