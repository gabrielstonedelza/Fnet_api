from django.db import models
from django.utils import timezone
from django.conf import settings

User = settings.AUTH_USER_MODEL
BANKS = (
    ("Access Bank", "Access Bank"),
    ("Cal Bank", "Cal Bank"),
    ("Fidelity Bank", "Fidelity Bank"),
    ("Ecobank", "Ecobank"),
    ("First Bank of Nigeria", "First Bank of Nigeria"),
    ("SGSSB", "SGSSB")
)

REQUEST_STATUS = (
    ("Approved", "Approved"),
    ("Pending", "Pending")
)

MODE_OF_PAYMENT = (
    ("Bank Payment", "Bank Payment"),
    ("Momo Payment", "Momo Payment"),
    ("Momo pay Payment", "Momo pay Payment"),
    ("Agent to Agent", "Agent to Agent"),
    ("Bank Payment", "Bank Payment"),
    ("Cash left @", "Cash left @"),
)

PAYMENT_OFFICES = (
    ("DVLA", "DVLA"),
    ("HEAD OFFICE", "HEAD OFFICE"),
    ("KEJETIA", "KEJETIA"),
    ("ECOBANK", "ECOBANK"),
    ("PAN AFRICA", "PAN AFRICA"),
)


class FNetAdmin(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Customer(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    account_number = models.CharField(max_length=16)
    bank = models.CharField(max_length=100, choices=BANKS, default="Access Bank")
    location = models.CharField(max_length=100)
    digital_address = models.CharField(max_length=15)
    phone = models.CharField(max_length=15)
    date_of_birth = models.CharField(max_length=15)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AgentDepositRequests(models.Model):
    guarantor = models.ForeignKey(FNetAdmin, on_delete=models.CASCADE, default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_requesting")
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agent_requesting")
    amount = models.CharField(max_length=500)
    bank = models.CharField(max_length=100, choices=BANKS, default="GT Bank")
    request_status = models.CharField(max_length=20, choices=REQUEST_STATUS, default="Pending")
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request made for {self.amount}"


class CustomerWithdrawal(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_withdrawing")
    bank = models.CharField(max_length=100, choices=BANKS, default="GT Bank")
    amount = models.CharField(max_length=500)
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.amount


class Payments(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    mode_of_payment = models.CharField(max_length=30, choices=MODE_OF_PAYMENT, blank=True)
    cash_at_location = models.CharField(max_length=30, choices=PAYMENT_OFFICES, blank=True)
    amount = models.CharField(max_length=500, blank=True)
    payment_status = models.CharField(max_length=20, choices=REQUEST_STATUS, default="Pending")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_status
