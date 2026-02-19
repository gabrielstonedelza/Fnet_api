"""
Two-Factor Authentication API views.

Endpoints:
  POST /api/v1/auth/2fa/setup/        — Generate secret + QR URI + backup codes
  POST /api/v1/auth/2fa/verify-setup/  — Confirm setup with a valid TOTP code
  POST /api/v1/auth/2fa/verify/        — Verify TOTP during login
  POST /api/v1/auth/2fa/disable/       — Disable 2FA (requires password + TOTP)
  GET  /api/v1/auth/2fa/status/        — Check 2FA status
  POST /api/v1/auth/2fa/backup-codes/  — Regenerate backup codes
"""

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .two_factor import TwoFactorAuth


@api_view(["GET"])
def twofa_status(request):
    """Check if 2FA is enabled for the current user."""
    try:
        tfa = request.user.two_factor
        return Response({
            "is_enabled": tfa.is_enabled,
            "is_verified": tfa.is_verified,
        })
    except TwoFactorAuth.DoesNotExist:
        return Response({
            "is_enabled": False,
            "is_verified": False,
        })


@api_view(["POST"])
def twofa_setup(request):
    """
    Begin 2FA setup.
    Generates a TOTP secret and returns the provisioning URI for QR scanning.
    Also generates 8 backup recovery codes.
    """
    # Delete any existing unverified setup
    TwoFactorAuth.objects.filter(user=request.user, is_verified=False).delete()

    # Check if already enabled
    if TwoFactorAuth.objects.filter(user=request.user, is_enabled=True).exists():
        return Response(
            {"error": "2FA is already enabled. Disable it first to reconfigure."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    secret = TwoFactorAuth.generate_secret()
    plain_codes, hashed_codes = TwoFactorAuth.generate_backup_codes()

    tfa = TwoFactorAuth.objects.create(
        user=request.user,
        secret=secret,
        is_enabled=False,
        is_verified=False,
        backup_codes=hashed_codes,
    )

    return Response({
        "secret": secret,
        "provisioning_uri": tfa.get_provisioning_uri(),
        "backup_codes": plain_codes,
        "message": (
            "Scan the QR code with your authenticator app (Google Authenticator, Authy, etc). "
            "Then submit a code to /2fa/verify-setup/ to activate. "
            "Save your backup codes — they won't be shown again."
        ),
    })


@api_view(["POST"])
def twofa_verify_setup(request):
    """
    Complete 2FA setup by verifying a TOTP code from the authenticator app.
    This activates 2FA on the account.
    """
    code = request.data.get("code", "").strip()
    if not code:
        return Response(
            {"error": "TOTP code is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        tfa = TwoFactorAuth.objects.get(user=request.user)
    except TwoFactorAuth.DoesNotExist:
        return Response(
            {"error": "No 2FA setup found. Call /2fa/setup/ first."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if tfa.is_enabled:
        return Response(
            {"error": "2FA is already enabled."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not tfa.verify_code(code):
        return Response(
            {"error": "Invalid code. Make sure your authenticator is synced."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    tfa.is_enabled = True
    tfa.is_verified = True
    tfa.save(update_fields=["is_enabled", "is_verified"])

    return Response({
        "message": "2FA is now enabled. You'll need your authenticator code to log in.",
        "is_enabled": True,
    })


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def twofa_verify_login(request):
    """
    Verify TOTP code during login.
    Called after initial login returns requires_2fa=True.
    Accepts either a 6-digit TOTP code or a backup code.
    """
    temp_token = request.data.get("temp_token", "").strip()
    code = request.data.get("code", "").strip()

    if not temp_token or not code:
        return Response(
            {"error": "Both temp_token and code are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Resolve user from temp token (stored as Token key)
    try:
        token_obj = Token.objects.select_related("user").get(key=temp_token)
        user = token_obj.user
    except Token.DoesNotExist:
        return Response(
            {"error": "Invalid or expired temporary token."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    try:
        tfa = user.two_factor
    except TwoFactorAuth.DoesNotExist:
        return Response(
            {"error": "2FA is not configured for this user."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Try TOTP first, then backup codes
    verified = tfa.verify_code(code)
    used_backup = False
    if not verified:
        verified = tfa.verify_backup_code(code)
        used_backup = True

    if not verified:
        return Response(
            {"error": "Invalid authentication code."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # 2FA passed — return the real token
    from .models import Membership
    from .serializers import UserSerializer, MembershipSerializer

    active_memberships = Membership.objects.filter(
        user=user, is_active=True,
    ).select_related("company", "branch")

    companies = [
        {"id": str(m.company_id), "name": m.company.name, "role": m.role}
        for m in active_memberships
    ]
    membership = active_memberships.first()

    response_data = {
        "token": token_obj.key,
        "user": UserSerializer(user).data,
        "membership": MembershipSerializer(membership).data,
        "companies": companies,
        "two_factor_verified": True,
    }

    if used_backup:
        remaining = len(tfa.backup_codes)
        response_data["warning"] = (
            f"You used a backup code. {remaining} backup codes remaining. "
            "Generate new backup codes in your security settings."
        )

    return Response(response_data)


@api_view(["POST"])
def twofa_disable(request):
    """
    Disable 2FA. Requires current password and a valid TOTP code.
    """
    password = request.data.get("password", "")
    code = request.data.get("code", "").strip()

    if not password or not code:
        return Response(
            {"error": "Password and TOTP code are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not request.user.check_password(password):
        return Response(
            {"error": "Incorrect password."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        tfa = request.user.two_factor
    except TwoFactorAuth.DoesNotExist:
        return Response(
            {"error": "2FA is not enabled."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not tfa.verify_code(code):
        return Response(
            {"error": "Invalid TOTP code."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    tfa.delete()

    return Response({
        "message": "2FA has been disabled.",
        "is_enabled": False,
    })


@api_view(["POST"])
def twofa_regenerate_backup_codes(request):
    """
    Regenerate backup codes. Requires a valid TOTP code.
    Old backup codes are invalidated.
    """
    code = request.data.get("code", "").strip()
    if not code:
        return Response(
            {"error": "TOTP code is required to regenerate backup codes."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        tfa = request.user.two_factor
    except TwoFactorAuth.DoesNotExist:
        return Response(
            {"error": "2FA is not enabled."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not tfa.verify_code(code):
        return Response(
            {"error": "Invalid TOTP code."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    plain_codes, hashed_codes = TwoFactorAuth.generate_backup_codes()
    tfa.backup_codes = hashed_codes
    tfa.save(update_fields=["backup_codes"])

    return Response({
        "backup_codes": plain_codes,
        "message": "New backup codes generated. Save them — they won't be shown again.",
    })
