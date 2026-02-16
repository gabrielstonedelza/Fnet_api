from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "saas_platform.core"
    label = "core"
    verbose_name = "Core (Companies & Subscriptions)"
