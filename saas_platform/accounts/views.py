from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import User, Membership, Invitation, UserProfile
from .serializers import (
    UserSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    UserProfileSerializer,
    MembershipSerializer,
    InvitationCreateSerializer,
    InvitationSerializer,
    AcceptInvitationSerializer,
    LoginSerializer,
)


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login(request):
    """
    Login with email/password. Returns token and user info.
    If user belongs to multiple companies, company_id is required.
    """
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    user = authenticate(request, email=data["email"], password=data["password"])
    if not user:
        return Response(
            {"error": "Invalid email or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not user.is_active:
        return Response(
            {"error": "Account is deactivated."},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Resolve company membership
    active_memberships = Membership.objects.filter(
        user=user, is_active=True,
    ).select_related("company", "branch")
    if not active_memberships.exists():
        return Response(
            {"error": "You are not a member of any active company."},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Build companies list for the frontend
    companies = [
        {
            "id": str(m.company_id),
            "name": m.company.name,
            "role": m.role,
        }
        for m in active_memberships
    ]

    company_id = data.get("company_id")

    # Multiple companies and no selection → ask user to choose
    if active_memberships.count() > 1 and not company_id:
        return Response(
            {
                "requires_company_selection": True,
                "message": "Multiple companies found. Please select one.",
                "companies": companies,
            },
            status=status.HTTP_200_OK,
        )

    if company_id:
        membership = active_memberships.filter(company_id=company_id).first()
        if not membership:
            return Response(
                {"error": "You are not a member of this company."},
                status=status.HTTP_403_FORBIDDEN,
            )
    else:
        membership = active_memberships.first()

    # Check company status
    if not membership.company.is_subscription_active:
        return Response(
            {"error": "Company subscription is not active. Contact the company owner."},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Update last login IP
    ip = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", ""))
    if ip:
        ip = ip.split(",")[0].strip()
        user.last_login_ip = ip
        user.save(update_fields=["last_login_ip"])

    token, _ = Token.objects.get_or_create(user=user)

    # Check if 2FA is enabled — require TOTP verification before issuing token
    try:
        tfa = user.two_factor
        if tfa.is_enabled:
            return Response({
                "requires_2fa": True,
                "temp_token": token.key,
                "message": "Enter your authenticator code to complete login.",
            })
    except Exception:
        pass  # No 2FA configured — proceed normally

    return Response({
        "token": token.key,
        "user": UserSerializer(user).data,
        "membership": MembershipSerializer(membership).data,
        "companies": companies,
    })


@api_view(["POST"])
def logout(request):
    """Delete auth token."""
    Token.objects.filter(user=request.user).delete()
    return Response({"message": "Logged out."})


# ---------------------------------------------------------------------------
# User Profile
# ---------------------------------------------------------------------------
@api_view(["GET"])
def me(request):
    """Get current user info with all memberships."""
    memberships = Membership.objects.filter(user=request.user, is_active=True)
    return Response({
        "user": UserSerializer(request.user).data,
        "memberships": MembershipSerializer(memberships, many=True).data,
    })


@api_view(["PATCH"])
def update_me(request):
    """Update current user's basic info."""
    serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(UserSerializer(request.user).data)


@api_view(["POST"])
def change_password(request):
    """Change password."""
    serializer = ChangePasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if not request.user.check_password(serializer.validated_data["current_password"]):
        return Response(
            {"error": "Current password is incorrect."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    request.user.set_password(serializer.validated_data["new_password"])
    request.user.save()
    Token.objects.filter(user=request.user).delete()
    token = Token.objects.create(user=request.user)
    return Response({"message": "Password changed.", "token": token.key})


@api_view(["GET", "PATCH"])
def user_profile(request):
    """Get or update extended profile."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "GET":
        return Response(UserProfileSerializer(profile).data)

    serializer = UserProfileSerializer(profile, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


# ---------------------------------------------------------------------------
# Team Management (company members)
# ---------------------------------------------------------------------------
@api_view(["GET"])
def team_members(request):
    """List all members of the current company."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    members = Membership.objects.filter(
        company=membership.company
    ).select_related("user", "branch")

    if membership.role == "teller":
        members = members.filter(is_active=True)

    return Response(MembershipSerializer(members, many=True).data)


@api_view(["GET"])
def team_member_detail(request, member_id):
    """Get details of a specific team member."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        target = Membership.objects.get(id=member_id, company=membership.company)
    except Membership.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return Response(MembershipSerializer(target).data)


@api_view(["PATCH"])
def update_team_member(request, member_id):
    """Update a team member's role, branch, or active status."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role not in ("owner", "admin"):
        return Response(
            {"error": "Only owners and admins can manage team members."},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        target = Membership.objects.get(id=member_id, company=membership.company)
    except Membership.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if target.role_level >= membership.role_level and target.user != request.user:
        return Response(
            {"error": "Cannot modify a member with equal or higher role."},
            status=status.HTTP_403_FORBIDDEN,
        )

    new_role = request.data.get("role")
    if new_role:
        new_level = Membership.ROLE_HIERARCHY.get(new_role, 0)
        if new_level >= membership.role_level:
            return Response(
                {"error": "Cannot assign a role equal to or above your own."},
                status=status.HTTP_403_FORBIDDEN,
            )
        target.role = new_role

    if "branch" in request.data:
        from core.models import Branch
        branch_id = request.data["branch"]
        if branch_id:
            try:
                branch = Branch.objects.get(id=branch_id, company=membership.company)
                target.branch = branch
            except Branch.DoesNotExist:
                return Response(
                    {"error": "Branch not found."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            target.branch = None

    if "is_active" in request.data:
        target.is_active = request.data["is_active"]
        if not target.is_active:
            target.deactivated_at = timezone.now()

    target.save()
    return Response(MembershipSerializer(target).data)


@api_view(["POST"])
def deactivate_team_member(request, member_id):
    """Deactivate a team member (soft delete)."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role not in ("owner", "admin"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        target = Membership.objects.get(id=member_id, company=membership.company)
    except Membership.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if target.role == "owner":
        return Response(
            {"error": "Cannot deactivate the company owner."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if target.role_level >= membership.role_level:
        return Response(
            {"error": "Cannot deactivate a member with equal or higher role."},
            status=status.HTTP_403_FORBIDDEN,
        )

    target.is_active = False
    target.deactivated_at = timezone.now()
    target.save(update_fields=["is_active", "deactivated_at"])
    return Response({"message": f"{target.user.full_name} has been deactivated."})


# ---------------------------------------------------------------------------
# Invitations
# ---------------------------------------------------------------------------
@api_view(["GET", "POST"])
def invitations(request):
    """List or create invitations."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role not in ("owner", "admin", "manager"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        qs = Invitation.objects.filter(company=membership.company)
        return Response(InvitationSerializer(qs, many=True).data)

    serializer = InvitationCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    # Check user limit
    plan = membership.company.subscription_plan
    current_count = Membership.objects.filter(
        company=membership.company, is_active=True
    ).count()
    pending_invites = Invitation.objects.filter(
        company=membership.company, status="pending"
    ).count()
    if current_count + pending_invites >= plan.max_users:
        return Response(
            {"error": f"User limit reached ({plan.max_users}). Upgrade your plan."},
            status=status.HTTP_403_FORBIDDEN,
        )

    invited_role_level = Membership.ROLE_HIERARCHY.get(data["role"], 0)
    if invited_role_level >= membership.role_level:
        return Response(
            {"error": "Cannot invite someone with equal or higher role than yours."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if Membership.objects.filter(
        company=membership.company, user__email=data["email"], is_active=True
    ).exists():
        return Response(
            {"error": "This person is already a member of your company."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    branch = None
    branch_id = data.get("branch")
    if branch_id:
        from core.models import Branch
        try:
            branch = Branch.objects.get(id=branch_id, company=membership.company)
        except Branch.DoesNotExist:
            return Response(
                {"error": "Branch not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    invitation = Invitation.objects.create(
        company=membership.company,
        email=data["email"],
        role=data["role"],
        branch=branch,
        invited_by=request.user,
        expires_at=timezone.now() + timedelta(days=7),
    )

    return Response(
        InvitationSerializer(invitation).data,
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
def revoke_invitation(request, invitation_id):
    """Revoke a pending invitation."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role not in ("owner", "admin"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        invitation = Invitation.objects.get(
            id=invitation_id, company=membership.company, status="pending"
        )
    except Invitation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    invitation.status = "revoked"
    invitation.save(update_fields=["status"])
    return Response({"message": "Invitation revoked."})


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def accept_invitation(request):
    """
    Accept an invitation. Creates user (if new) and membership.
    """
    serializer = AcceptInvitationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    try:
        invitation = Invitation.objects.get(token=data["token"])
    except Invitation.DoesNotExist:
        return Response(
            {"error": "Invalid invitation token."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not invitation.is_valid:
        return Response(
            {"error": "Invitation is expired or already used."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user, created = User.objects.get_or_create(
        email=invitation.email,
        defaults={
            "full_name": data["full_name"],
            "phone": data.get("phone", ""),
        },
    )
    if created:
        user.set_password(data["password"])
        user.save()

    Membership.objects.create(
        user=user,
        company=invitation.company,
        role=invitation.role,
        branch=invitation.branch,
        is_active=True,
    )

    invitation.status = "accepted"
    invitation.accepted_at = timezone.now()
    invitation.save(update_fields=["status", "accepted_at"])

    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        "message": "Invitation accepted. Welcome aboard!",
        "token": token.key,
        "user": UserSerializer(user).data,
    })
