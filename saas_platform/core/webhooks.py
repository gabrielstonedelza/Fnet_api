"""
Webhook system for Merchant+ — outbound event delivery.

Companies can register webhook URLs to receive real-time events:
  - transaction.created
  - transaction.completed
  - transaction.reversed
  - customer.created
  - customer.kyc_verified
  - balance.changed

Events are delivered via HTTP POST with HMAC-SHA256 signature for verification.
"""

import hashlib
import hmac
import json
import logging
import uuid
from datetime import datetime

from django.db import models

logger = logging.getLogger(__name__)


class WebhookEndpoint(models.Model):
    """A company's registered webhook URL."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        "core.Company", on_delete=models.CASCADE, related_name="webhook_endpoints"
    )
    url = models.URLField(max_length=500)
    secret = models.CharField(
        max_length=64,
        help_text="HMAC secret for signing payloads. Auto-generated.",
    )
    events = models.JSONField(
        default=list,
        help_text="List of event types to subscribe to. Empty = all events.",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_triggered_at = models.DateTimeField(null=True, blank=True)
    failure_count = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = "core"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Webhook {self.url} ({self.company.name})"

    @staticmethod
    def generate_secret():
        import secrets
        return secrets.token_hex(32)


class WebhookDelivery(models.Model):
    """Log of webhook delivery attempts."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    endpoint = models.ForeignKey(
        WebhookEndpoint, on_delete=models.CASCADE, related_name="deliveries"
    )
    event_type = models.CharField(max_length=50)
    payload = models.JSONField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    response_status_code = models.IntegerField(null=True, blank=True)
    response_body = models.TextField(blank=True)
    attempts = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "core"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.event_type} → {self.endpoint.url} ({self.status})"


def sign_payload(payload: dict, secret: str) -> str:
    """Create HMAC-SHA256 signature for a webhook payload."""
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    return hmac.new(
        secret.encode("utf-8"),
        body.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def dispatch_webhook(company_id: str, event_type: str, data: dict):
    """
    Queue webhook delivery for all matching endpoints of a company.
    Called from signals after transaction/customer events.
    """
    try:
        from core.webhooks import WebhookEndpoint

        endpoints = WebhookEndpoint.objects.filter(
            company_id=company_id,
            is_active=True,
            failure_count__lt=10,  # Disable after 10 consecutive failures
        )

        for endpoint in endpoints:
            # Filter by subscribed events
            if endpoint.events and event_type not in endpoint.events:
                continue

            payload = {
                "id": str(uuid.uuid4()),
                "event": event_type,
                "created_at": datetime.utcnow().isoformat() + "Z",
                "data": data,
            }

            WebhookDelivery.objects.create(
                endpoint=endpoint,
                event_type=event_type,
                payload=payload,
            )

        # Trigger async delivery
        from core.tasks import deliver_pending_webhooks
        deliver_pending_webhooks.delay(company_id)

    except Exception as e:
        logger.error("Failed to dispatch webhook %s: %s", event_type, e)
