from django.apps import AppConfig


class CustomersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "saas_platform.customers"
    label = "customers"
    verbose_name = "Customers"
