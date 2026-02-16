from rest_framework import serializers
from .models import Notification, ActivityLog


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id", "category", "title", "message",
            "is_read", "read_at", "related_object_id", "created_at",
        ]
        read_only_fields = ["id", "category", "title", "message", "related_object_id", "created_at"]


class ActivityLogSerializer(serializers.ModelSerializer):
    actor_name = serializers.CharField(source="actor.full_name", read_only=True, default=None)

    class Meta:
        model = ActivityLog
        fields = [
            "id", "actor", "actor_name",
            "action_type", "description", "metadata",
            "ip_address", "created_at",
        ]
