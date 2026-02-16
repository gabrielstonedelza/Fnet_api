import uuid
from django.db import models


class Customer(models.Model):
    """
    A customer registered by a company's staff.
    Customers are scoped to a company (tenant).
    """

    class KYCStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        VERIFIED = "verified", "Verified"
        REJECTED = "rejected", "Rejected"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        BLOCKED = "blocked", "Blocked"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        "core.Company", on_delete=models.CASCADE, related_name="customers"
    )
    registered_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="registered_customers",
    )
    branch = models.ForeignKey(
        "core.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customers",
    )

    # Personal info
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    digital_address = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(upload_to="customer_photos/", blank=True, null=True)

    # Identification (KYC)
    id_type = models.CharField(
        max_length=30,
        choices=[
            ("passport", "Passport"),
            ("national_id", "National ID / Ghana Card"),
            ("drivers_license", "Driver's License"),
            ("voter_id", "Voter ID"),
        ],
        blank=True,
    )
    id_number = models.CharField(max_length=50, blank=True)
    id_document_front = models.ImageField(
        upload_to="customer_ids/", blank=True, null=True
    )
    id_document_back = models.ImageField(
        upload_to="customer_ids/", blank=True, null=True
    )
    kyc_status = models.CharField(
        max_length=20, choices=KYCStatus.choices, default=KYCStatus.PENDING
    )
    kyc_verified_at = models.DateTimeField(null=True, blank=True)
    kyc_verified_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_customers",
    )

    # Status
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )

    # Loyalty
    loyalty_points = models.PositiveIntegerField(default=0)

    # Referral
    referred_by = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referrals",
    )

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = [["company", "phone"]]

    def __str__(self):
        return f"{self.full_name} ({self.phone})"


class CustomerAccount(models.Model):
    """Bank or mobile money accounts belonging to a customer."""

    class AccountType(models.TextChoices):
        BANK = "bank", "Bank Account"
        MOBILE_MONEY = "mobile_money", "Mobile Money"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="accounts"
    )
    company = models.ForeignKey(
        "core.Company", on_delete=models.CASCADE, related_name="customer_accounts"
    )

    account_type = models.CharField(max_length=20, choices=AccountType.choices)
    account_number = models.CharField(max_length=50)
    account_name = models.CharField(max_length=255)
    bank_or_network = models.CharField(
        max_length=100,
        help_text="Bank name (e.g. Ecobank, GCB) or mobile network (e.g. MTN, Vodafone).",
    )
    is_primary = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_primary", "-created_at"]

    def __str__(self):
        return f"{self.account_name} - {self.bank_or_network} ({self.account_number})"
