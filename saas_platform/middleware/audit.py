"""
Audit Middleware.

Stores the current request in thread-local storage so that audit utilities
can access it from anywhere (views, signals, etc.).
"""

import threading

_local = threading.local()


def get_current_request():
    """Utility to access the current request from anywhere (e.g., signals)."""
    return getattr(_local, "request", None)


class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _local.request = request
        response = self.get_response(request)
        _local.request = None
        return response
