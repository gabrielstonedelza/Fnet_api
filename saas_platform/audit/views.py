from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import AuditEntry
from .serializers import AuditEntrySerializer


@api_view(["GET"])
def audit_log(request):
    """View the company audit trail. Owner/Admin only."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role not in ("owner", "admin"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    if not membership.company.subscription_plan.has_audit_trail:
        return Response(
            {"error": "Audit trail is not available on your plan. Upgrade to access."},
            status=status.HTTP_403_FORBIDDEN,
        )

    qs = AuditEntry.objects.filter(company=membership.company).select_related("actor")

    action = request.query_params.get("action")
    if action:
        qs = qs.filter(action=action)

    resource_type = request.query_params.get("resource_type")
    if resource_type:
        qs = qs.filter(resource_type=resource_type)

    actor_id = request.query_params.get("actor")
    if actor_id:
        qs = qs.filter(actor_id=actor_id)

    date_from = request.query_params.get("date_from")
    if date_from:
        qs = qs.filter(timestamp__date__gte=date_from)

    date_to = request.query_params.get("date_to")
    if date_to:
        qs = qs.filter(timestamp__date__lte=date_to)

    search = request.query_params.get("search")
    if search:
        qs = qs.filter(resource_repr__icontains=search)

    return Response(AuditEntrySerializer(qs[:500], many=True).data)


@api_view(["GET"])
def audit_entry_detail(request, entry_id):
    """View a single audit entry with full change details."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role not in ("owner", "admin"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        entry = AuditEntry.objects.get(id=entry_id, company=membership.company)
    except AuditEntry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return Response(AuditEntrySerializer(entry).data)
