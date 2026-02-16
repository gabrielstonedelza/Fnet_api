from django.contrib import admin
from .models import Customer, CustomerAccount


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        "full_name", "phone", "company", "status",
        "kyc_status", "loyalty_points", "created_at",
    ]
    list_filter = ["status", "kyc_status", "company"]
    search_fields = ["full_name", "phone", "email"]
    raw_id_fields = ["company", "registered_by", "branch", "referred_by"]
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(CustomerAccount)
class CustomerAccountAdmin(admin.ModelAdmin):
    list_display = [
        "account_name", "account_number", "bank_or_network",
        "account_type", "customer", "is_primary",
    ]
    list_filter = ["account_type", "is_verified"]
    search_fields = ["account_name", "account_number", "customer__full_name"]
