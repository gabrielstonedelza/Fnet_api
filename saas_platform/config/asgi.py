"""ASGI config for the SaaS Financial Platform."""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saas_platform.config.settings")

application = get_asgi_application()
