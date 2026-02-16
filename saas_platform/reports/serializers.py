from rest_framework import serializers
from .models import SavedReport


class SavedReportSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source="created_by.full_name", read_only=True)

    class Meta:
        model = SavedReport
        fields = [
            "id", "name", "report_type", "filters",
            "is_scheduled", "schedule_frequency",
            "created_by", "created_by_name",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]
