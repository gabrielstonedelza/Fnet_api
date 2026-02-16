from django.apps import AppConfig


class TransactionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "transactions"
    verbose_name = "Transactions"

    def ready(self):
        import transactions.signals  # noqa: F401
