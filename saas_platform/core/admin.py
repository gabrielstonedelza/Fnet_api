from django.contrib import admin
from .models import SubscriptionPlan, Company, Branch, APIKey, CompanySettings
from .webhooks import WebhookEndpoint, WebhookDelivery


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ["name", "tier", "monthly_price", "max_users", "max_customers", "is_active"]
    list_filter = ["tier", "is_active"]
    search_fields = ["name"]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        "name", "slug", "email", "subscription_plan", "subscription_status",
        "status", "is_verified", "created_at",
    ]
    list_filter = ["status", "subscription_status", "is_verified", "subscription_plan"]
    search_fields = ["name", "email", "slug"]
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ["name", "company", "city", "is_headquarters", "is_active"]
    list_filter = ["is_headquarters", "is_active"]
    search_fields = ["name", "company__name"]


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ["name", "company", "key_prefix", "is_active", "last_used_at", "created_at"]
    list_filter = ["is_active"]
    search_fields = ["name", "company__name"]


@admin.register(CompanySettings)
class CompanySettingsAdmin(admin.ModelAdmin):
    list_display = ["company", "default_currency", "require_approval_above"]
    search_fields = ["company__name"]


@admin.register(WebhookEndpoint)
class WebhookEndpointAdmin(admin.ModelAdmin):
    list_display = ["url", "company", "is_active", "failure_count", "last_triggered_at"]
    list_filter = ["is_active"]
    search_fields = ["url", "company__name"]
    readonly_fields = ["id", "secret", "created_at"]


@admin.register(WebhookDelivery)
class WebhookDeliveryAdmin(admin.ModelAdmin):
    list_display = ["event_type", "endpoint", "status", "response_status_code", "attempts", "created_at"]
    list_filter = ["status", "event_type"]
    readonly_fields = ["id", "payload", "response_body", "created_at"]
