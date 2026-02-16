"""WSGI config for the SaaS Financial Platform."""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saas_platform.config.settings")

application = get_wsgi_application()
