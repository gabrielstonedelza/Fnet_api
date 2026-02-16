from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("transactions/", views.transaction_summary, name="transaction-summary"),
    path("agents/", views.agent_performance, name="agent-performance"),
    path("revenue/", views.revenue_report, name="revenue-report"),
    path("saved/", views.saved_reports, name="saved-reports"),
    path("saved/<uuid:report_id>/", views.delete_saved_report, name="delete-saved-report"),
]
