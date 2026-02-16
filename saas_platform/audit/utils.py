"""Utility functions for creating audit entries from anywhere."""

from .models import AuditEntry
from middleware.audit import get_current_request


def log_audit(
    action, resource_type, resource_id="", resource_repr="",
    changes=None, company=None, actor=None,
):
    """
    Create an audit entry.
    Automatically picks up IP/user-agent from the current request if available.
    """
    request = get_current_request()

    if request and not actor:
        actor = request.user if request.user.is_authenticated else None
    if request and not company:
        company = getattr(request, "company", None)

    ip = None
    user_agent = ""
    endpoint = ""
    if request:
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
        ip = forwarded.split(",")[0].strip() if forwarded else request.META.get("REMOTE_ADDR")
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        endpoint = f"{request.method} {request.path}"

    AuditEntry.objects.create(
        company=company, actor=actor, action=action,
        resource_type=resource_type, resource_id=str(resource_id),
        resource_repr=resource_repr, changes=changes or {},
        ip_address=ip, user_agent=user_agent, endpoint=endpoint,
    )
