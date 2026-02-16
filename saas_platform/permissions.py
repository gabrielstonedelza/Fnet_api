"""
Role-based access control permissions for the SaaS platform.

Role Hierarchy:
    Owner (4) > Admin (3) > Manager (2) > Teller (1)

Usage in views:
    from permissions import IsCompanyMember, IsAdminOrAbove

    @api_view(["GET"])
    @permission_classes([IsAuthenticated, IsCompanyMember])
    def my_view(request):
        ...
"""

from rest_framework.permissions import BasePermission


class IsCompanyMember(BasePermission):
    """User must have an active membership in a company."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and getattr(request, "membership", None) is not None
        )


class IsOwner(BasePermission):
    """User must be the company owner."""

    def has_permission(self, request, view):
        membership = getattr(request, "membership", None)
        return membership and membership.role == "owner"


class IsAdminOrAbove(BasePermission):
    """User must be admin or owner."""

    def has_permission(self, request, view):
        membership = getattr(request, "membership", None)
        return membership and membership.role in ("owner", "admin")


class IsManagerOrAbove(BasePermission):
    """User must be manager, admin, or owner."""

    def has_permission(self, request, view):
        membership = getattr(request, "membership", None)
        return membership and membership.role in ("owner", "admin", "manager")


class IsCompanyActive(BasePermission):
    """Company must have an active subscription."""

    message = "Company subscription is not active."

    def has_permission(self, request, view):
        membership = getattr(request, "membership", None)
        if not membership:
            return False
        return membership.company.is_subscription_active


class ReadOnly(BasePermission):
    """Allow only safe (read-only) methods."""

    def has_permission(self, request, view):
        return request.method in ("GET", "HEAD", "OPTIONS")
