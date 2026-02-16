from rest_framework import serializers
from .models import SubscriptionPlan, Company, Branch, APIKey, CompanySettings


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = [
            "id", "name", "tier", "description",
            "max_users", "max_customers", "max_transactions_per_month",
            "has_reports", "has_audit_trail", "has_api_access",
            "has_mobile_money", "has_bank_deposits", "has_multi_branch",
            "monthly_price", "annual_price", "currency",
        ]


class CompanyRegistrationSerializer(serializers.Serializer):
    """Used when a new company owner signs up."""

    # Company details
    company_name = serializers.CharField(max_length=255)
    company_email = serializers.EmailField()
    company_phone = serializers.CharField(max_length=20)
    company_address = serializers.CharField(required=False, allow_blank=True)
    company_city = serializers.CharField(max_length=100, required=False, allow_blank=True)
    company_country = serializers.CharField(max_length=100, default="Ghana")
    business_registration_number = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )

    # Owner details
    owner_email = serializers.EmailField()
    owner_phone = serializers.CharField(max_length=20)
    owner_full_name = serializers.CharField(max_length=255)
    owner_password = serializers.CharField(min_length=8, write_only=True)

    # Plan
    subscription_plan = serializers.UUIDField()


class CompanySerializer(serializers.ModelSerializer):
    subscription_plan_name = serializers.CharField(
        source="subscription_plan.name", read_only=True
    )
    owner_name = serializers.CharField(source="owner.full_name", read_only=True)
    is_subscription_active = serializers.BooleanField(read_only=True)
    user_count = serializers.SerializerMethodField()
    customer_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = [
            "id", "name", "slug", "email", "phone", "address", "city",
            "country", "logo", "business_registration_number", "tax_id",
            "subscription_plan", "subscription_plan_name",
            "subscription_status", "trial_ends_at",
            "subscription_started_at", "subscription_ends_at",
            "status", "is_verified", "is_subscription_active",
            "owner", "owner_name",
            "user_count", "customer_count",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "slug", "subscription_status", "trial_ends_at",
            "subscription_started_at", "subscription_ends_at",
            "status", "is_verified", "owner", "created_at", "updated_at",
        ]

    def get_user_count(self, obj):
        return obj.members.count()

    def get_customer_count(self, obj):
        return obj.customers.count()


class CompanyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "name", "email", "phone", "address", "city",
            "country", "logo", "business_registration_number", "tax_id",
        ]


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = [
            "id", "company", "name", "address", "city", "phone",
            "is_headquarters", "is_active", "created_at",
        ]
        read_only_fields = ["id", "company", "created_at"]


class APIKeyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = ["name", "expires_at"]


class APIKeySerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(
        source="created_by.full_name", read_only=True
    )

    class Meta:
        model = APIKey
        fields = [
            "id", "name", "key_prefix", "is_active",
            "last_used_at", "expires_at",
            "created_by", "created_by_name", "created_at",
        ]
        read_only_fields = [
            "id", "key_prefix", "last_used_at",
            "created_by", "created_at",
        ]


class CompanySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySettings
        fields = [
            "require_approval_above", "default_currency", "allow_overdraft",
            "deposit_fee_percentage", "withdrawal_fee_percentage",
            "transfer_fee_flat",
            "notify_on_large_transaction", "large_transaction_threshold",
            "daily_summary_email",
            "enable_loyalty_points", "points_per_transaction",
        ]
