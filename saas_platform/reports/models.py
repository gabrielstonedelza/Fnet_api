import uuid
from django.db import models


class SavedReport(models.Model):
    """Saved/scheduled report configurations."""

    class ReportType(models.TextChoices):
        TRANSACTION_SUMMARY = "transaction_summary", "Transaction Summary"
        AGENT_PERFORMANCE = "agent_performance", "Agent Performance"
        CUSTOMER_ACTIVITY = "customer_activity", "Customer Activity"
        REVENUE_REPORT = "revenue_report", "Revenue Report"
        DAILY_RECONCILIATION = "daily_reconciliation", "Daily Reconciliation"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        "core.Company", on_delete=models.CASCADE, related_name="saved_reports"
    )
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="saved_reports",
    )
    name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=30, choices=ReportType.choices)
    filters = models.JSONField(default=dict, help_text="Saved filter configuration.")
    is_scheduled = models.BooleanField(default=False)
    schedule_frequency = models.CharField(
        max_length=20,
        choices=[("daily", "Daily"), ("weekly", "Weekly"), ("monthly", "Monthly")],
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.name} ({self.report_type})"
