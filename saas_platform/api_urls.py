"""
API v1 URL routing.
All endpoints are prefixed with /api/v1/ via config/urls.py.
"""

from django.urls import path, include

urlpatterns = [
    path("", include("core.urls")),
    path("auth/", include("accounts.urls")),
    path("customers/", include("customers.urls")),
    path("transactions/", include("transactions.urls")),
    path("notifications/", include("notifications.urls")),
    path("reports/", include("reports.urls")),
    path("audit/", include("audit.urls")),
]
