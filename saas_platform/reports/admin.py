from django.contrib import admin
from .models import SavedReport


@admin.register(SavedReport)
class SavedReportAdmin(admin.ModelAdmin):
    list_display = ["name", "report_type", "company", "created_by", "is_scheduled", "created_at"]
    list_filter = ["report_type", "is_scheduled", "company"]
    search_fields = ["name", "company__name"]
