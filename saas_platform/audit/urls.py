from django.urls import path
from . import views

app_name = "audit"

urlpatterns = [
    path("", views.audit_log, name="audit-log"),
    path("<uuid:entry_id>/", views.audit_entry_detail, name="audit-detail"),
]
