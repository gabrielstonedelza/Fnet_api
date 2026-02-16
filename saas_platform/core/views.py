import hashlib
from django.utils import timezone
from django.utils.text import slugify
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from datetime import timedelta

from .models import SubscriptionPlan, Company, Branch, APIKey, CompanySettings
from .serializers import (
    SubscriptionPlanSerializer,
    CompanyRegistrationSerializer,
    CompanySerializer,
    CompanyUpdateSerializer,
    BranchSerializer,
    APIKeyCreateSerializer,
    APIKeySerializer,
    CompanySettingsSerializer,
)


# ---------------------------------------------------------------------------
# Public: Subscription Plans
# ---------------------------------------------------------------------------
class SubscriptionPlanListView(generics.ListAPIView):
    """Public endpoint to list available subscription plans."""

    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]


# ---------------------------------------------------------------------------
# Company Registration (Public)
# ---------------------------------------------------------------------------
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register_company(request):
    """
    Register a new company and its owner in one step.
    Creates: Company, Owner User, CompanySettings, default HQ Branch.
    """
    from accounts.models import User, Membership

    serializer = CompanyRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    # Validate plan exists
    try:
        plan = SubscriptionPlan.objects.get(id=data["subscription_plan"], is_active=True)
    except SubscriptionPlan.DoesNotExist:
        return Response(
            {"error": "Invalid subscription plan."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check email uniqueness
    if User.objects.filter(email=data["owner_email"]).exists():
        return Response(
            {"error": "A user with this email already exists."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Create company
    base_slug = slugify(data["company_name"])
    slug = base_slug
    counter = 1
    while Company.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    company = Company.objects.create(
        name=data["company_name"],
        slug=slug,
        email=data["company_email"],
        phone=data["company_phone"],
        address=data.get("company_address", ""),
        city=data.get("company_city", ""),
        country=data.get("company_country", "Ghana"),
        business_registration_number=data.get("business_registration_number", ""),
        subscription_plan=plan,
        subscription_status="trial",
        trial_ends_at=timezone.now() + timedelta(days=14),
    )

    # Create owner user
    owner = User.objects.create_user(
        email=data["owner_email"],
        phone=data["owner_phone"],
        full_name=data["owner_full_name"],
        password=data["owner_password"],
        is_active=True,
    )

    # Link owner to company
    company.owner = owner
    company.save(update_fields=["owner"])

    # Create membership
    Membership.objects.create(
        user=owner,
        company=company,
        role=Membership.Role.OWNER,
        is_active=True,
    )

    # Create default settings
    CompanySettings.objects.create(company=company)

    # Create default HQ branch
    Branch.objects.create(
        company=company,
        name="Headquarters",
        is_headquarters=True,
    )

    return Response(
        {
            "message": "Company registered successfully.",
            "company": CompanySerializer(company).data,
        },
        status=status.HTTP_201_CREATED,
    )


# ---------------------------------------------------------------------------
# Company Detail / Update (Owner / Admin only)
# ---------------------------------------------------------------------------
@api_view(["GET"])
def get_my_company(request):
    """Get the current user's company details."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(
            {"error": "You are not a member of any company."},
            status=status.HTTP_403_FORBIDDEN,
        )
    serializer = CompanySerializer(membership.company)
    return Response(serializer.data)


@api_view(["PATCH"])
def update_company(request):
    """Update company details. Owner/Admin only."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role not in ("owner", "admin"):
        return Response(
            {"error": "Only owners and admins can update company details."},
            status=status.HTTP_403_FORBIDDEN,
        )
    serializer = CompanyUpdateSerializer(
        membership.company, data=request.data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(CompanySerializer(membership.company).data)


# ---------------------------------------------------------------------------
# Branch Management
# ---------------------------------------------------------------------------
@api_view(["GET", "POST"])
def branches(request):
    """List or create branches for the current company."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        qs = Branch.objects.filter(company=membership.company)
        return Response(BranchSerializer(qs, many=True).data)

    # POST - owner/admin only
    if membership.role not in ("owner", "admin"):
        return Response(
            {"error": "Only owners and admins can create branches."},
            status=status.HTTP_403_FORBIDDEN,
        )
    if not membership.company.subscription_plan.has_multi_branch:
        existing = Branch.objects.filter(company=membership.company).count()
        if existing >= 1:
            return Response(
                {"error": "Your plan does not support multiple branches. Upgrade to add more."},
                status=status.HTTP_403_FORBIDDEN,
            )
    serializer = BranchSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(company=membership.company)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
def branch_detail(request, branch_id):
    """Retrieve, update, or delete a branch."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        branch = Branch.objects.get(id=branch_id, company=membership.company)
    except Branch.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(BranchSerializer(branch).data)

    if membership.role not in ("owner", "admin"):
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == "PATCH":
        serializer = BranchSerializer(branch, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    if request.method == "DELETE":
        if branch.is_headquarters:
            return Response(
                {"error": "Cannot delete the headquarters branch."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        branch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------------------------------------------------------------------------
# API Key Management (Owner only)
# ---------------------------------------------------------------------------
@api_view(["GET", "POST"])
def api_keys(request):
    """List or create API keys."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role != "owner":
        return Response(
            {"error": "Only the company owner can manage API keys."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if not membership.company.subscription_plan.has_api_access:
        return Response(
            {"error": "Your plan does not include API access."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "GET":
        qs = APIKey.objects.filter(company=membership.company)
        return Response(APIKeySerializer(qs, many=True).data)

    serializer = APIKeyCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    raw_key = APIKey.generate_key()
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()

    api_key = APIKey.objects.create(
        company=membership.company,
        name=serializer.validated_data["name"],
        key_prefix=raw_key[:8],
        key_hash=key_hash,
        expires_at=serializer.validated_data.get("expires_at"),
        created_by=request.user,
    )

    return Response(
        {
            "key": raw_key,
            "detail": APIKeySerializer(api_key).data,
            "warning": "Store this key securely. It will not be shown again.",
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["DELETE"])
def revoke_api_key(request, key_id):
    """Revoke (deactivate) an API key."""
    membership = getattr(request, "membership", None)
    if not membership or membership.role != "owner":
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        api_key = APIKey.objects.get(id=key_id, company=membership.company)
    except APIKey.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    api_key.is_active = False
    api_key.save(update_fields=["is_active"])
    return Response({"message": "API key revoked."})


# ---------------------------------------------------------------------------
# Company Settings
# ---------------------------------------------------------------------------
@api_view(["GET", "PATCH"])
def company_settings(request):
    """Get or update company settings."""
    membership = getattr(request, "membership", None)
    if not membership:
        return Response(status=status.HTTP_403_FORBIDDEN)

    settings_obj, _ = CompanySettings.objects.get_or_create(
        company=membership.company
    )

    if request.method == "GET":
        return Response(CompanySettingsSerializer(settings_obj).data)

    if membership.role not in ("owner", "admin"):
        return Response(
            {"error": "Only owners and admins can update settings."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = CompanySettingsSerializer(
        settings_obj, data=request.data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
