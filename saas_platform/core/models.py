import uuid
import secrets
from django.db import models
from django.utils import timezone


class SubscriptionPlan(models.Model):
    """Defines the tiers available for companies subscribing to the platform."""

    class Tier(models.TextChoices):
        FREE = "free", "Free"
        STARTER = "starter", "Starter"
        PROFESSIONAL = "professional", "Professional"
        ENTERPRISE = "enterprise", "Enterprise"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    tier = models.CharField(max_length=20, choices=Tier.choices, unique=True)
    description = models.TextField(blank=True)

    # Limits
    max_users = models.PositiveIntegerField(
        help_text="Maximum number of staff users the company can have."
    )
    max_customers = models.PositiveIntegerField(
        help_text="Maximum number of customers the company can register."
    )
    max_transactions_per_month = models.PositiveIntegerField(
        help_text="Maximum transactions per month. 0 = unlimited.",
        default=0,
    )

    # Features
    has_reports = models.BooleanField(default=False)
    has_audit_trail = models.BooleanField(default=False)
    has_api_access = models.BooleanField(default=False)
    has_mobile_money = models.BooleanField(default=True)
    has_bank_deposits = models.BooleanField(default=True)
    has_multi_branch = models.BooleanField(default=False)

    # Pricing
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    annual_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default="GHS")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["monthly_price"]

    def __str__(self):
        return f"{self.name} ({self.tier})"


class Company(models.Model):
    """
    The tenant. Every company is an isolated workspace.
    All data (users, customers, transactions) belongs to a company.
    """

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        SUSPENDED = "suspended", "Suspended"
        DEACTIVATED = "deactivated", "Deactivated"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default="Ghana")
    logo = models.ImageField(upload_to="company_logos/", blank=True, null=True)

    # Registration info
    business_registration_number = models.CharField(max_length=100, blank=True)
    tax_id = models.CharField(max_length=100, blank=True)

    # Subscription
    subscription_plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        related_name="companies",
    )
    subscription_status = models.CharField(
        max_length=20,
        choices=[
            ("active", "Active"),
            ("trial", "Trial"),
            ("past_due", "Past Due"),
            ("cancelled", "Cancelled"),
        ],
        default="trial",
    )
    trial_ends_at = models.DateTimeField(null=True, blank=True)
    subscription_started_at = models.DateTimeField(null=True, blank=True)
    subscription_ends_at = models.DateTimeField(null=True, blank=True)

    # Status
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )
    is_verified = models.BooleanField(default=False)

    # Owner
    owner = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="owned_companies",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "companies"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def is_on_trial(self):
        if self.subscription_status != "trial":
            return False
        if self.trial_ends_at and self.trial_ends_at < timezone.now():
            return False
        return True

    @property
    def is_subscription_active(self):
        if self.status != self.Status.ACTIVE:
            return False
        if self.subscription_status == "trial":
            return self.is_on_trial
        if self.subscription_status == "active":
            if self.subscription_ends_at:
                return self.subscription_ends_at > timezone.now()
            return True
        return False


class Branch(models.Model):
    """Physical branches/locations for a company."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="branches"
    )
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_headquarters = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "branches"
        ordering = ["-is_headquarters", "name"]
        unique_together = [["company", "name"]]

    def __str__(self):
        return f"{self.name} ({self.company.name})"


class APIKey(models.Model):
    """API keys for companies that have API access enabled."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="api_keys"
    )
    name = models.CharField(max_length=100, help_text="Label for this API key.")
    key_prefix = models.CharField(max_length=8)
    key_hash = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_api_keys",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.key_prefix}...)"

    @staticmethod
    def generate_key():
        return secrets.token_urlsafe(48)


class CompanySettings(models.Model):
    """Per-company configuration."""

    company = models.OneToOneField(
        Company, on_delete=models.CASCADE, related_name="settings"
    )

    # Transaction settings
    require_approval_above = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=1000.00,
        help_text="Transactions above this amount require manager/admin approval.",
    )
    default_currency = models.CharField(max_length=3, default="GHS")
    allow_overdraft = models.BooleanField(default=False)

    # Fee settings
    deposit_fee_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00
    )
    withdrawal_fee_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00
    )
    transfer_fee_flat = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )

    # Notification preferences
    notify_on_large_transaction = models.BooleanField(default=True)
    large_transaction_threshold = models.DecimalField(
        max_digits=12, decimal_places=2, default=5000.00
    )
    daily_summary_email = models.BooleanField(default=False)

    # Loyalty
    enable_loyalty_points = models.BooleanField(default=False)
    points_per_transaction = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "company settings"

    def __str__(self):
        return f"Settings for {self.company.name}"
