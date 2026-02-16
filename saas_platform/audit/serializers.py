from rest_framework import serializers
from .models import AuditEntry


class AuditEntrySerializer(serializers.ModelSerializer):
    actor_name = serializers.CharField(source="actor.full_name", read_only=True, default=None)
    actor_email = serializers.CharField(source="actor.email", read_only=True, default=None)

    class Meta:
        model = AuditEntry
        fields = [
            "id", "actor", "actor_name", "actor_email",
            "action", "resource_type", "resource_id", "resource_repr",
            "changes", "ip_address", "user_agent", "endpoint", "timestamp",
        ]
