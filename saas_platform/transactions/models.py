import uuid
from django.db import models


class Transaction(models.Model):
    """
    Central transaction record. Every financial operation creates one of these.
    This is the single source of truth for all money movement.
    """

    class Type(models.TextChoices):
        DEPOSIT = "deposit", "Deposit"
        WITHDRAWAL = "withdrawal", "Withdrawal"
        TRANSFER = "transfer", "Transfer"
        FEE = "fee", "Fee"
        COMMISSION = "commission", "Commission"
        REVERSAL = "reversal", "Reversal"

    class Channel(models.TextChoices):
        BANK = "bank", "Bank"
        MOBILE_MONEY = "mobile_money", "Mobile Money"
        CASH = "cash", "Cash"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        COMPLETED = "completed", "Completed"
        REJECTED = "rejected", "Rejected"
        REVERSED = "reversed", "Reversed"
        FAILED = "failed", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=30, unique=True, editable=False)
    company = models.ForeignKey(
        "core.Company", on_delete=models.CASCADE, related_name="transactions"
    )
    branch = models.ForeignKey(
        "core.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
    )
    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
    )

    # Who initiated this transaction
    initiated_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="initiated_transactions",
    )

    # Transaction details
    transaction_type = models.CharField(max_length=20, choices=Type.choices)
    channel = models.CharField(max_length=20, choices=Channel.choices)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )

    amount = models.DecimalField(max_digits=14, decimal_places=2)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        help_text="Amount after fees. Computed on save.",
    )
    currency = models.CharField(max_length=3, default="GHS")

    description = models.TextField(blank=True)
    internal_notes = models.TextField(
        blank=True, help_text="Notes visible only to company staff."
    )

    # Approval workflow
    requires_approval = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_transactions",
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    # Reversal link
    reversed_transaction = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reversals",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["company", "created_at"]),
            models.Index(fields=["company", "status"]),
            models.Index(fields=["company", "transaction_type"]),
            models.Index(fields=["reference"]),
        ]

    def __str__(self):
        return f"{self.reference} - {self.transaction_type} {self.amount} {self.currency}"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._generate_reference()
        if self.net_amount is None:
            self.net_amount = self.amount - self.fee
        super().save(*args, **kwargs)

    @staticmethod
    def _generate_reference():
        import time
        import random
        timestamp = int(time.time() * 1000)
        rand = random.randint(100, 999)
        return f"TXN-{timestamp}-{rand}"


class BankDeposit(models.Model):
    """Extended details for bank deposit transactions."""

    transaction = models.OneToOneField(
        Transaction, on_delete=models.CASCADE, related_name="bank_deposit_detail"
    )
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    account_name = models.CharField(max_length=255)
    depositor_name = models.CharField(max_length=255)
    slip_number = models.CharField(max_length=50, blank=True)
    slip_image = models.ImageField(upload_to="deposit_slips/", blank=True, null=True)

    def __str__(self):
        return f"Bank deposit {self.transaction.reference} to {self.bank_name}"


class MobileMoneyTransaction(models.Model):
    """Extended details for mobile money transactions."""

    class Network(models.TextChoices):
        MTN = "mtn", "MTN"
        VODAFONE = "vodafone", "Vodafone"
        AIRTELTIGO = "airteltigo", "AirtelTigo"

    class ServiceType(models.TextChoices):
        SEND_MONEY = "send_money", "Send Money"
        RECEIVE_MONEY = "receive_money", "Receive Money"
        CASH_IN = "cash_in", "Cash In"
        CASH_OUT = "cash_out", "Cash Out"

    transaction = models.OneToOneField(
        Transaction, on_delete=models.CASCADE, related_name="momo_detail"
    )
    network = models.CharField(max_length=20, choices=Network.choices)
    service_type = models.CharField(max_length=20, choices=ServiceType.choices)
    sender_number = models.CharField(max_length=20)
    receiver_number = models.CharField(max_length=20, blank=True)
    momo_reference = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"MoMo {self.service_type} - {self.network} ({self.transaction.reference})"


class CashTransaction(models.Model):
    """Extended details for cash transactions."""

    transaction = models.OneToOneField(
        Transaction, on_delete=models.CASCADE, related_name="cash_detail"
    )
    d_200 = models.PositiveIntegerField(default=0, verbose_name="200 GHS notes")
    d_100 = models.PositiveIntegerField(default=0, verbose_name="100 GHS notes")
    d_50 = models.PositiveIntegerField(default=0, verbose_name="50 GHS notes")
    d_20 = models.PositiveIntegerField(default=0, verbose_name="20 GHS notes")
    d_10 = models.PositiveIntegerField(default=0, verbose_name="10 GHS notes")
    d_5 = models.PositiveIntegerField(default=0, verbose_name="5 GHS notes")
    d_2 = models.PositiveIntegerField(default=0, verbose_name="2 GHS coins")
    d_1 = models.PositiveIntegerField(default=0, verbose_name="1 GHS coins")

    @property
    def denomination_total(self):
        return (
            self.d_200 * 200 + self.d_100 * 100 + self.d_50 * 50 +
            self.d_20 * 20 + self.d_10 * 10 + self.d_5 * 5 +
            self.d_2 * 2 + self.d_1 * 1
        )

    def __str__(self):
        return f"Cash detail for {self.transaction.reference}"


class ExpenseRequest(models.Model):
    """Internal expense requests by staff."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        PAID = "paid", "Paid"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        "core.Company", on_delete=models.CASCADE, related_name="expense_requests"
    )
    requested_by = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="expense_requests",
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    approved_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="approved_expenses",
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    receipt_image = models.ImageField(
        upload_to="expense_receipts/", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Expense {self.amount} by {self.requested_by.full_name}"


class DailyClosing(models.Model):
    """
    End-of-day account closing record per user per branch.
    Tracks all balances at close of business.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        "core.Company", on_delete=models.CASCADE, related_name="daily_closings"
    )
    branch = models.ForeignKey(
        "core.Branch", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="daily_closings",
    )
    closed_by = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="daily_closings",
    )

    date = models.DateField()

    physical_cash = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    mtn_ecash = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    vodafone_ecash = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    airteltigo_ecash = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_ecash = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    overage = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shortage = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]
        unique_together = [["company", "closed_by", "date"]]

    def __str__(self):
        return f"Closing {self.date} by {self.closed_by.full_name}"


class ProviderBalance(models.Model):
    """
    Tracks agent float balances per provider for each user in a company.
    Each user starts with a configured amount for each provider (MTN, Vodafone,
    Airtel, Tigo, Ecobank, Fidelity, Cal Bank) and the balance changes as
    they process deposits and withdrawals.
    """

    class Provider(models.TextChoices):
        MTN = "mtn", "MTN"
        VODAFONE = "vodafone", "Vodafone"
        AIRTEL = "airtel", "Airtel"
        TIGO = "tigo", "Tigo"
        ECOBANK = "ecobank", "Ecobank"
        FIDELITY = "fidelity", "Fidelity"
        CAL_BANK = "cal_bank", "Cal Bank"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        "core.Company", on_delete=models.CASCADE, related_name="provider_balances"
    )
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="provider_balances"
    )
    provider = models.CharField(max_length=20, choices=Provider.choices)
    starting_balance = models.DecimalField(
        max_digits=14, decimal_places=2, default=0,
        help_text="The float amount the agent started with for this provider.",
    )
    balance = models.DecimalField(
        max_digits=14, decimal_places=2, default=0,
        help_text="Current running balance for this provider.",
    )
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["company", "user", "provider"]]
        ordering = ["provider"]
        indexes = [
            models.Index(fields=["company", "user"]),
        ]

    def __str__(self):
        return f"{self.user.full_name} - {self.get_provider_display()}: {self.balance}"
