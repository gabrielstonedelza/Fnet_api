"""
Two-Factor Authentication (TOTP) for Merchant+.

Implements RFC 6238 Time-Based One-Time Password using pyotp.
Provides:
  - TOTP secret generation + QR provisioning URI
  - Code verification
  - Backup codes for account recovery
  - 2FA enforcement on login

Security+ alignment:
  - 4.0: Multi-factor authentication (something you know + something you have)
  - 3.0: Identity and access management
"""

import uuid
import secrets
import hashlib
from django.db import models
from django.conf import settings


class TwoFactorAuth(models.Model):
    """
    TOTP 2FA configuration for a user.
    Stores the shared secret and backup recovery codes.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="two_factor",
    )
    secret = models.CharField(
        max_length=64,
        help_text="Base32-encoded TOTP secret.",
    )
    is_enabled = models.BooleanField(
        default=False,
        help_text="2FA is only active after the user confirms setup with a valid code.",
    )
    is_verified = models.BooleanField(
        default=False,
        help_text="Set to True after user successfully verifies during setup.",
    )
    backup_codes = models.JSONField(
        default=list,
        help_text="Hashed backup recovery codes.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "accounts"
        verbose_name = "Two-Factor Auth"
        verbose_name_plural = "Two-Factor Auth"

    def __str__(self):
        status = "enabled" if self.is_enabled else "disabled"
        return f"2FA ({status}) for {self.user.email}"

    @staticmethod
    def generate_secret():
        """Generate a new Base32-encoded TOTP secret."""
        import pyotp
        return pyotp.random_base32(length=32)

    def get_totp(self):
        """Get a pyotp TOTP instance for this user."""
        import pyotp
        return pyotp.TOTP(self.secret)

    def get_provisioning_uri(self):
        """
        Get the otpauth:// URI for QR code generation.
        Compatible with Google Authenticator, Authy, etc.
        """
        totp = self.get_totp()
        return totp.provisioning_uri(
            name=self.user.email,
            issuer_name="Merchant+",
        )

    def verify_code(self, code: str) -> bool:
        """Verify a 6-digit TOTP code. Allows 1-step time drift."""
        totp = self.get_totp()
        return totp.verify(code, valid_window=1)

    def verify_backup_code(self, code: str) -> bool:
        """
        Verify and consume a backup code.
        Each backup code can only be used once.
        """
        code_hash = self._hash_code(code)
        if code_hash in self.backup_codes:
            self.backup_codes.remove(code_hash)
            self.save(update_fields=["backup_codes"])
            return True
        return False

    @staticmethod
    def generate_backup_codes(count: int = 8) -> tuple[list[str], list[str]]:
        """
        Generate backup recovery codes.
        Returns (plain_codes, hashed_codes).
        Plain codes are shown to user once; hashed codes are stored.
        """
        plain_codes = []
        hashed_codes = []
        for _ in range(count):
            code = secrets.token_hex(4).upper()  # e.g., "A1B2C3D4"
            plain_codes.append(code)
            hashed_codes.append(TwoFactorAuth._hash_code(code))
        return plain_codes, hashed_codes

    @staticmethod
    def _hash_code(code: str) -> str:
        """Hash a backup code for storage."""
        return hashlib.sha256(code.strip().upper().encode()).hexdigest()
