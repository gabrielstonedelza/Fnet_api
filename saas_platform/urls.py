"""
SaaS Platform API URL Configuration.

All endpoints are prefixed with /api/v1/ in the main project urls.py.
"""

from django.urls import path, include

urlpatterns = [
    path("", include("saas_platform.core.urls")),
    path("auth/", include("saas_platform.accounts.urls")),
    path("customers/", include("saas_platform.customers.urls")),
    path("transactions/", include("saas_platform.transactions.urls")),
    path("notifications/", include("saas_platform.notifications.urls")),
    path("reports/", include("saas_platform.reports.urls")),
    path("audit/", include("saas_platform.audit.urls")),
]
