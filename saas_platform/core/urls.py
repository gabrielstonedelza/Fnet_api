from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    # Public
    path("plans/", views.SubscriptionPlanListView.as_view(), name="plan-list"),
    path("register/", views.register_company, name="register-company"),

    # Company (authenticated)
    path("company/", views.get_my_company, name="my-company"),
    path("company/update/", views.update_company, name="update-company"),
    path("company/settings/", views.company_settings, name="company-settings"),

    # Branches
    path("branches/", views.branches, name="branch-list-create"),
    path("branches/<uuid:branch_id>/", views.branch_detail, name="branch-detail"),

    # API Keys
    path("api-keys/", views.api_keys, name="api-key-list-create"),
    path("api-keys/<uuid:key_id>/revoke/", views.revoke_api_key, name="api-key-revoke"),
]
