import uuid
from django.db import models


class Notification(models.Model):
    """In-app notifications for users."""

    class Category(models.TextChoices):
        TRANSACTION = "transaction", "Transaction"
        APPROVAL = "approval", "Approval"
        TEAM = "team", "Team"
        SYSTEM = "system", "System"
        CUSTOMER = "customer", "Customer"
        SECURITY = "security", "Security"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        "core.Company", on_delete=models.CASCADE, related_name="notifications"
    )
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="notifications",
    )
    category = models.CharField(max_length=20, choices=Category.choices)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    related_object_id = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "is_read"]),
            models.Index(fields=["company", "created_at"]),
        ]

    def __str__(self):
        return f"{self.title} -> {self.user.full_name}"


class ActivityLog(models.Model):
    """Company-wide activity feed visible to admins."""

    class ActionType(models.TextChoices):
        CUSTOMER_CREATED = "customer_created", "Customer Created"
        CUSTOMER_UPDATED = "customer_updated", "Customer Updated"
        TRANSACTION_CREATED = "transaction_created", "Transaction Created"
        TRANSACTION_APPROVED = "transaction_approved", "Transaction Approved"
        TRANSACTION_REJECTED = "transaction_rejected", "Transaction Rejected"
        TRANSACTION_REVERSED = "transaction_reversed", "Transaction Reversed"
        USER_INVITED = "user_invited", "User Invited"
        USER_JOINED = "user_joined", "User Joined"
        USER_DEACTIVATED = "user_deactivated", "User Deactivated"
        EXPENSE_SUBMITTED = "expense_submitted", "Expense Submitted"
        EXPENSE_APPROVED = "expense_approved", "Expense Approved"
        SETTINGS_CHANGED = "settings_changed", "Settings Changed"
        DAILY_CLOSING = "daily_closing", "Daily Closing"
        KYC_VERIFIED = "kyc_verified", "KYC Verified"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        "core.Company", on_delete=models.CASCADE, related_name="activity_logs"
    )
    actor = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True,
        related_name="activity_logs",
    )
    action_type = models.CharField(max_length=30, choices=ActionType.choices)
    description = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["company", "created_at"]),
            models.Index(fields=["company", "action_type"]),
        ]

    def __str__(self):
        return f"{self.action_type} by {self.actor} at {self.created_at}"
