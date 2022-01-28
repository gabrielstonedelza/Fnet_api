from django.apps import AppConfig


class FnetApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fnet_api'

    def ready(self):
        import fnet_api.signals
