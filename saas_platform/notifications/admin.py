from django.contrib import admin
from .models import Notification, ActivityLog


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "user", "company", "is_read", "created_at"]
    list_filter = ["category", "is_read", "company"]
    search_fields = ["title", "message", "user__full_name"]


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ["action_type", "actor", "company", "description", "created_at"]
    list_filter = ["action_type", "company"]
    search_fields = ["description", "actor__full_name"]
    readonly_fields = ["id", "created_at"]
