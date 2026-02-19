"""
Celery tasks for notifications and scheduled reports.
"""

import logging
from datetime import date, timedelta
from decimal import Decimal

from celery import shared_task
from django.db.models import Sum, Count

logger = logging.getLogger(__name__)


@shared_task(name="notifications.send_daily_summaries")
def send_daily_summaries():
    """
    Send daily summary email to all company admins/owners who have it enabled.
    Scheduled via Celery Beat at end of business day.
    """
    from core.models import CompanySettings
    from accounts.models import Membership
    from transactions.models import Transaction
    from customers.models import Customer
    from .email import send_daily_summary

    today = date.today()
    enabled_settings = CompanySettings.objects.filter(daily_summary_email=True).select_related("company")

    for cs in enabled_settings:
        company = cs.company
        if not company.is_subscription_active:
            continue

        today_txns = Transaction.objects.filter(company=company, created_at__date=today)

        summary = {
            "total_transactions": today_txns.count(),
            "total_deposits": str(
                today_txns.filter(transaction_type="deposit", status="completed")
                .aggregate(t=Sum("amount"))["t"] or Decimal("0")
            ),
            "total_withdrawals": str(
                today_txns.filter(transaction_type="withdrawal", status="completed")
                .aggregate(t=Sum("amount"))["t"] or Decimal("0")
            ),
            "total_fees": str(
                today_txns.filter(status="completed")
                .aggregate(t=Sum("fee"))["t"] or Decimal("0")
            ),
            "pending_approvals": Transaction.objects.filter(
                company=company, requires_approval=True, status="pending"
            ).count(),
        }

        # Send to all owners and admins
        admin_memberships = Membership.objects.filter(
            company=company, is_active=True, role__in=["owner", "admin"]
        ).select_related("user")

        for m in admin_memberships:
            send_daily_summary(m.user.email, m.user.full_name, company.name, summary)
            logger.info("Sent daily summary to %s for %s", m.user.email, company.name)


@shared_task(name="notifications.send_transaction_alert_task")
def send_transaction_alert_task(user_email: str, user_name: str, tx_data: dict):
    """Async wrapper for transaction alert emails."""
    from .email import send_transaction_alert
    send_transaction_alert(user_email, user_name, tx_data)


@shared_task(name="notifications.send_transaction_sms_task")
def send_transaction_sms_task(phone: str, tx_data: dict):
    """Async wrapper for transaction SMS alerts."""
    from .sms import send_transaction_sms
    send_transaction_sms(phone, tx_data)


@shared_task(name="notifications.send_security_sms_task")
def send_security_sms_task(phone: str, event: str):
    """Async wrapper for security SMS alerts."""
    from .sms import send_security_sms
    send_security_sms(phone, event)


@shared_task(name="notifications.send_approval_sms_task")
def send_approval_sms_task(phone: str, reference: str, amount: str):
    """Async wrapper for approval SMS alerts."""
    from .sms import send_approval_sms
    send_approval_sms(phone, reference, amount)


@shared_task(name="notifications.cleanup_old_notifications")
def cleanup_old_notifications(days: int = 90):
    """Remove read notifications older than N days."""
    from django.utils import timezone
    from .models import Notification

    cutoff = timezone.now() - timedelta(days=days)
    deleted, _ = Notification.objects.filter(is_read=True, created_at__lt=cutoff).delete()
    logger.info("Cleaned up %d old notifications", deleted)
