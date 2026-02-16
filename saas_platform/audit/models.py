import uuid
from django.db import models


class AuditEntry(models.Model):
    """
    Immutable audit trail record.
    Records every significant data change for compliance.
    """

    class Action(models.TextChoices):
        CREATE = "create", "Create"
        UPDATE = "update", "Update"
        DELETE = "delete", "Delete"
        LOGIN = "login", "Login"
        LOGOUT = "logout", "Logout"
        LOGIN_FAILED = "login_failed", "Login Failed"
        PASSWORD_CHANGE = "password_change", "Password Change"
        PERMISSION_CHANGE = "permission_change", "Permission Change"
        EXPORT = "export", "Data Export"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        "core.Company", on_delete=models.CASCADE,
        related_name="audit_entries", null=True, blank=True,
    )
    actor = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="audit_entries",
    )
    action = models.CharField(max_length=20, choices=Action.choices)

    resource_type = models.CharField(max_length=50, help_text="Model name, e.g. 'Transaction'")
    resource_id = models.CharField(max_length=50, blank=True)
    resource_repr = models.CharField(max_length=255, blank=True)

    changes = models.JSONField(
        default=dict, blank=True,
        help_text="JSON of changed fields: {field: {old: x, new: y}}",
    )

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    endpoint = models.CharField(max_length=500, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name_plural = "audit entries"
        indexes = [
            models.Index(fields=["company", "timestamp"]),
            models.Index(fields=["company", "resource_type"]),
            models.Index(fields=["actor", "timestamp"]),
        ]

    def __str__(self):
        return f"{self.action} {self.resource_type} by {self.actor} at {self.timestamp}"
