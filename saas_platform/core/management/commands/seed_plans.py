"""
Management command to create default subscription plans.

Usage:
    python manage.py seed_plans
"""

from django.core.management.base import BaseCommand
from core.models import SubscriptionPlan


PLANS = [
    {
        "name": "Free",
        "tier": "free",
        "description": "Get started with basic financial operations.",
        "max_users": 2,
        "max_customers": 50,
        "max_transactions_per_month": 200,
        "has_reports": False,
        "has_audit_trail": False,
        "has_api_access": False,
        "has_mobile_money": True,
        "has_bank_deposits": True,
        "has_multi_branch": False,
        "monthly_price": 0,
        "annual_price": 0,
    },
    {
        "name": "Starter",
        "tier": "starter",
        "description": "For small businesses getting started with financial services.",
        "max_users": 5,
        "max_customers": 500,
        "max_transactions_per_month": 2000,
        "has_reports": True,
        "has_audit_trail": False,
        "has_api_access": False,
        "has_mobile_money": True,
        "has_bank_deposits": True,
        "has_multi_branch": False,
        "monthly_price": 99.00,
        "annual_price": 990.00,
    },
    {
        "name": "Professional",
        "tier": "professional",
        "description": "For growing businesses that need advanced features and multiple branches.",
        "max_users": 25,
        "max_customers": 5000,
        "max_transactions_per_month": 0,
        "has_reports": True,
        "has_audit_trail": True,
        "has_api_access": True,
        "has_mobile_money": True,
        "has_bank_deposits": True,
        "has_multi_branch": True,
        "monthly_price": 299.00,
        "annual_price": 2990.00,
    },
    {
        "name": "Enterprise",
        "tier": "enterprise",
        "description": "For large organizations with custom requirements and unlimited scale.",
        "max_users": 100,
        "max_customers": 50000,
        "max_transactions_per_month": 0,
        "has_reports": True,
        "has_audit_trail": True,
        "has_api_access": True,
        "has_mobile_money": True,
        "has_bank_deposits": True,
        "has_multi_branch": True,
        "monthly_price": 799.00,
        "annual_price": 7990.00,
    },
]


class Command(BaseCommand):
    help = "Create default subscription plans"

    def handle(self, *args, **options):
        for plan_data in PLANS:
            plan, created = SubscriptionPlan.objects.update_or_create(
                tier=plan_data["tier"],
                defaults=plan_data,
            )
            action = "Created" if created else "Updated"
            self.stdout.write(f"  {action}: {plan.name} ({plan.tier})")

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. {SubscriptionPlan.objects.count()} plans available."
        ))
