from django.apps import AppConfig


class CustomersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "customers"
    verbose_name = "Customers"

    def ready(self):
        import customers.signals  # noqa: F401
