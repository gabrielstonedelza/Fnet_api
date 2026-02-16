from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction


@receiver(post_save, sender=Transaction)
def transaction_post_save(sender, instance, created, **kwargs):
    """Create notifications for new transactions and status changes."""
    from saas_platform.notifications.models import Notification

    if created:
        # Notify the company owner/admins about large transactions
        company = instance.company
        settings = getattr(company, "settings", None)
        if settings and settings.notify_on_large_transaction:
            if instance.amount >= settings.large_transaction_threshold:
                from saas_platform.accounts.models import Membership
                admin_memberships = Membership.objects.filter(
                    company=company,
                    role__in=["owner", "admin"],
                    is_active=True,
                )
                for m in admin_memberships:
                    Notification.objects.create(
                        company=company,
                        user=m.user,
                        category=Notification.Category.TRANSACTION,
                        title="Large Transaction Alert",
                        message=(
                            f"A {instance.transaction_type} of {instance.amount} "
                            f"{instance.currency} ({instance.reference}) was initiated "
                            f"by {instance.initiated_by.full_name if instance.initiated_by else 'System'}."
                        ),
                        related_object_id=str(instance.id),
                    )

        # Notify if approval is required
        if instance.requires_approval and instance.status == "pending":
            from saas_platform.accounts.models import Membership
            approver_memberships = Membership.objects.filter(
                company=company,
                role__in=["owner", "admin", "manager"],
                is_active=True,
            ).exclude(user=instance.initiated_by)
            for m in approver_memberships:
                Notification.objects.create(
                    company=company,
                    user=m.user,
                    category=Notification.Category.APPROVAL,
                    title="Approval Required",
                    message=(
                        f"{instance.initiated_by.full_name if instance.initiated_by else 'Someone'} "
                        f"submitted a {instance.transaction_type} of {instance.amount} "
                        f"{instance.currency} that requires your approval."
                    ),
                    related_object_id=str(instance.id),
                )
