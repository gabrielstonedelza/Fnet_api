from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction, ProviderBalance


@receiver(post_save, sender=Transaction)
def transaction_post_save(sender, instance, created, **kwargs):
    """Create notifications and broadcast real-time events for transactions."""
    from notifications.models import Notification

    if created:
        company = instance.company
        settings = getattr(company, "settings", None)

        # Notify admins about large transactions
        if settings and settings.notify_on_large_transaction:
            if instance.amount >= settings.large_transaction_threshold:
                from accounts.models import Membership
                admin_memberships = Membership.objects.filter(
                    company=company, role__in=["owner", "admin"], is_active=True,
                )
                for m in admin_memberships:
                    Notification.objects.create(
                        company=company, user=m.user,
                        category=Notification.Category.TRANSACTION,
                        title="Large Transaction Alert",
                        message=(
                            f"A {instance.transaction_type} of {instance.amount} "
                            f"{instance.currency} ({instance.reference}) was initiated "
                            f"by {instance.initiated_by.full_name if instance.initiated_by else 'System'}."
                        ),
                        related_object_id=str(instance.id),
                    )

        # Notify approvers if approval required
        if instance.requires_approval and instance.status == "pending":
            from accounts.models import Membership
            approver_memberships = Membership.objects.filter(
                company=company, role__in=["owner", "admin", "manager"],
                is_active=True,
            ).exclude(user=instance.initiated_by)
            for m in approver_memberships:
                Notification.objects.create(
                    company=company, user=m.user,
                    category=Notification.Category.APPROVAL,
                    title="Approval Required",
                    message=(
                        f"{instance.initiated_by.full_name if instance.initiated_by else 'Someone'} "
                        f"submitted a {instance.transaction_type} of {instance.amount} "
                        f"{instance.currency} that requires your approval."
                    ),
                    related_object_id=str(instance.id),
                )

    # Broadcast transaction event to admin dashboard via WebSocket
    try:
        from .broadcast import broadcast_to_company
        broadcast_to_company(
            company_id=str(instance.company_id),
            event_type="transaction_event",
            data={
                "type": "transaction_update",
                "transaction": {
                    "id": str(instance.id),
                    "reference": instance.reference,
                    "transaction_type": instance.transaction_type,
                    "channel": instance.channel,
                    "status": instance.status,
                    "amount": str(instance.amount),
                    "fee": str(instance.fee),
                    "net_amount": str(instance.net_amount),
                    "currency": instance.currency,
                    "customer_name": instance.customer.full_name if instance.customer else None,
                    "initiated_by_name": instance.initiated_by.full_name if instance.initiated_by else None,
                    "created_at": instance.created_at.isoformat() if instance.created_at else None,
                    "is_new": created,
                },
            },
        )
    except Exception:
        pass  # Don't break transactions if WebSocket layer is unavailable


@receiver(post_save, sender=ProviderBalance)
def provider_balance_post_save(sender, instance, **kwargs):
    """Broadcast balance changes to admin dashboard."""
    try:
        from .broadcast import broadcast_to_company
        broadcast_to_company(
            company_id=str(instance.company_id),
            event_type="balance_event",
            data={
                "type": "balance_change",
                "balance": {
                    "user_id": str(instance.user_id),
                    "user_name": instance.user.full_name,
                    "provider": instance.provider,
                    "balance": str(instance.balance),
                    "starting_balance": str(instance.starting_balance),
                },
            },
        )
    except Exception:
        pass
