from django.contrib import admin
from .models import AuditEntry


@admin.register(AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = [
        "action", "resource_type", "resource_repr",
        "actor", "company", "ip_address", "timestamp",
    ]
    list_filter = ["action", "resource_type", "company"]
    search_fields = ["resource_repr", "actor__full_name", "actor__email"]
    readonly_fields = [
        "id", "company", "actor", "action",
        "resource_type", "resource_id", "resource_repr",
        "changes", "ip_address", "user_agent", "endpoint", "timestamp",
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
