from rest_framework import serializers
from .models import SavedReport


class SavedReportSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(
        source="created_by.full_name", read_only=True
    )

    class Meta:
        model = SavedReport
        fields = [
            "id", "name", "report_type", "filters",
            "is_scheduled", "schedule_frequency",
            "created_by", "created_by_name",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]


class DashboardSummarySerializer(serializers.Serializer):
    """Read-only serializer for dashboard data."""
    total_transactions_today = serializers.IntegerField()
    total_deposits_today = serializers.DecimalField(max_digits=14, decimal_places=2)
    total_withdrawals_today = serializers.DecimalField(max_digits=14, decimal_places=2)
    total_fees_today = serializers.DecimalField(max_digits=14, decimal_places=2)
    pending_approvals = serializers.IntegerField()
    total_customers = serializers.IntegerField()
    total_active_users = serializers.IntegerField()
    transactions_by_channel = serializers.DictField()
    transactions_by_status = serializers.DictField()
    recent_transactions = serializers.ListField()
    top_agents = serializers.ListField()
