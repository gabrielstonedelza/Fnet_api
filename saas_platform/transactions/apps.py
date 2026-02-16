from django.apps import AppConfig


class TransactionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "saas_platform.transactions"
    label = "transactions"
    verbose_name = "Transactions"

    def ready(self):
        import saas_platform.transactions.signals  # noqa: F401
