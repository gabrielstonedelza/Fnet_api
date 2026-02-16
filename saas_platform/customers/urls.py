from django.urls import path
from . import views

app_name = "customers"

urlpatterns = [
    path("", views.customers, name="customer-list-create"),
    path("lookup/", views.customer_by_phone, name="customer-lookup"),
    path("<uuid:customer_id>/", views.customer_detail, name="customer-detail"),
    path("<uuid:customer_id>/kyc/", views.verify_kyc, name="customer-kyc"),
    path("<uuid:customer_id>/accounts/", views.customer_accounts, name="customer-accounts"),
    path(
        "<uuid:customer_id>/accounts/<uuid:account_id>/",
        views.delete_customer_account,
        name="customer-account-delete",
    ),
]
