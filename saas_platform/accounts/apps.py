from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "saas_platform.accounts"
    label = "accounts"
    verbose_name = "Accounts (Users & Roles)"

    def ready(self):
        import saas_platform.accounts.signals  # noqa: F401
