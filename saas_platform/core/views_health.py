"""
Health check endpoints for load balancers, Docker, and monitoring.

  GET /api/v1/health/       — Liveness: is the process running?
  GET /api/v1/health/ready/ — Readiness: can the app serve traffic?
"""

from django.db import connection
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """Liveness probe — always returns 200 if the process is up."""
    return Response({"status": "healthy", "service": "merchantplus-api"})


@api_view(["GET"])
@permission_classes([AllowAny])
def readiness_check(request):
    """
    Readiness probe — checks all downstream dependencies.
    Returns 503 if any dependency is unavailable.
    """
    checks = {}
    all_ok = True

    # Database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"error: {e}"
        all_ok = False

    # Redis / Channel Layer
    try:
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)("health-check", {"type": "health.check"})
        async_to_sync(channel_layer.receive)("health-check")
        checks["channel_layer"] = "ok"
    except Exception:
        checks["channel_layer"] = "unavailable (non-critical)"

    # Celery broker (optional)
    try:
        from config.celery import app as celery_app

        conn = celery_app.connection()
        conn.ensure_connection(max_retries=1, timeout=2)
        conn.close()
        checks["celery_broker"] = "ok"
    except Exception:
        checks["celery_broker"] = "unavailable (non-critical)"

    http_status = status.HTTP_200_OK if all_ok else status.HTTP_503_SERVICE_UNAVAILABLE
    return Response({"status": "ready" if all_ok else "degraded", "checks": checks}, status=http_status)
