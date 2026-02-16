from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "saas_platform.notifications"
    label = "notifications"
    verbose_name = "Notifications"
