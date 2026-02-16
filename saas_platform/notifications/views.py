from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Notification, ActivityLog
from .serializers import NotificationSerializer, ActivityLogSerializer


@api_view(["GET"])
def my_notifications(request):
    """Get current user's notifications."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    qs = Notification.objects.filter(company=membership.company, user=request.user)

    unread_only = request.query_params.get("unread")
    if unread_only == "true":
        qs = qs.filter(is_read=False)

    category = request.query_params.get("category")
    if category:
        qs = qs.filter(category=category)

    return Response(NotificationSerializer(qs[:100], many=True).data)


@api_view(["GET"])
def unread_count(request):
    """Get count of unread notifications."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    count = Notification.objects.filter(
        company=membership.company, user=request.user, is_read=False,
    ).count()
    return Response({"unread_count": count})


@api_view(["POST"])
def mark_read(request, notification_id):
    """Mark a single notification as read."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        notification = Notification.objects.get(
            id=notification_id, company=membership.company, user=request.user,
        )
    except Notification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    notification.is_read = True
    notification.read_at = timezone.now()
    notification.save(update_fields=["is_read", "read_at"])
    return Response(NotificationSerializer(notification).data)


@api_view(["POST"])
def mark_all_read(request):
    """Mark all notifications as read."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    Notification.objects.filter(
        company=membership.company, user=request.user, is_read=False,
    ).update(is_read=True, read_at=timezone.now())
    return Response({"message": "All notifications marked as read."})


@api_view(["GET"])
def activity_feed(request):
    """Get the company activity feed. Manager+ only."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role not in ("owner", "admin", "manager"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    qs = ActivityLog.objects.filter(company=membership.company).select_related("actor")

    action_type = request.query_params.get("action_type")
    if action_type:
        qs = qs.filter(action_type=action_type)

    date_from = request.query_params.get("date_from")
    if date_from:
        qs = qs.filter(created_at__date__gte=date_from)

    date_to = request.query_params.get("date_to")
    if date_to:
        qs = qs.filter(created_at__date__lte=date_to)

    actor_id = request.query_params.get("actor")
    if actor_id:
        qs = qs.filter(actor_id=actor_id)

    return Response(ActivityLogSerializer(qs[:200], many=True).data)
