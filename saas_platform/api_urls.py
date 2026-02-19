"""
API v1 URL routing.
All endpoints are prefixed with /api/v1/ via config/urls.py.
"""

from django.urls import path, include

from core.views_health import health_check, readiness_check
from core.webhook_views import webhook_endpoints, delete_webhook_endpoint, webhook_deliveries
from reports.export import export_transactions_csv, export_agents_csv

urlpatterns = [
    path("", include("core.urls")),
    path("auth/", include("accounts.urls")),
    path("customers/", include("customers.urls")),
    path("transactions/", include("transactions.urls")),
    path("notifications/", include("notifications.urls")),
    path("reports/", include("reports.urls")),
    path("audit/", include("audit.urls")),

    # Health checks (public)
    path("health/", health_check, name="health-check"),
    path("health/ready/", readiness_check, name="readiness-check"),

    # CSV Report Exports
    path("reports/export/transactions/", export_transactions_csv, name="export-transactions-csv"),
    path("reports/export/agents/", export_agents_csv, name="export-agents-csv"),

    # Webhook Management
    path("webhooks/", webhook_endpoints, name="webhook-list-create"),
    path("webhooks/<uuid:endpoint_id>/", delete_webhook_endpoint, name="webhook-delete"),
    path("webhooks/<uuid:endpoint_id>/deliveries/", webhook_deliveries, name="webhook-deliveries"),
]
