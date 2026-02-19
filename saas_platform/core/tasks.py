"""
Celery tasks for core operations — webhook delivery, cleanup.
"""

import json
import logging

import requests
from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)

WEBHOOK_TIMEOUT = 10  # seconds
MAX_RETRIES = 3


@shared_task(name="core.deliver_pending_webhooks", bind=True, max_retries=3)
def deliver_pending_webhooks(self, company_id: str):
    """Deliver all pending webhook payloads for a company."""
    from core.webhooks import WebhookDelivery, sign_payload

    pending = WebhookDelivery.objects.filter(
        endpoint__company_id=company_id,
        status="pending",
    ).select_related("endpoint")[:50]

    for delivery in pending:
        endpoint = delivery.endpoint
        payload = delivery.payload
        signature = sign_payload(payload, endpoint.secret)

        headers = {
            "Content-Type": "application/json",
            "X-Webhook-Signature": signature,
            "X-Webhook-Event": delivery.event_type,
            "User-Agent": "MerchantPlus-Webhook/1.0",
        }

        try:
            resp = requests.post(
                endpoint.url,
                json=payload,
                headers=headers,
                timeout=WEBHOOK_TIMEOUT,
            )
            delivery.response_status_code = resp.status_code
            delivery.response_body = resp.text[:1000]
            delivery.attempts += 1

            if 200 <= resp.status_code < 300:
                delivery.status = "success"
                endpoint.failure_count = 0
                endpoint.last_triggered_at = timezone.now()
                endpoint.save(update_fields=["failure_count", "last_triggered_at"])
            else:
                delivery.status = "failed"
                endpoint.failure_count += 1
                endpoint.save(update_fields=["failure_count"])

        except requests.RequestException as e:
            delivery.attempts += 1
            delivery.status = "failed"
            delivery.response_body = str(e)[:500]
            endpoint.failure_count += 1
            endpoint.save(update_fields=["failure_count"])
            logger.warning("Webhook delivery failed for %s: %s", endpoint.url, e)

        delivery.save()
