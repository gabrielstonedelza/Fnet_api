import uuid
import secrets
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model. Users are global but belong to companies via Membership.
    A user can belong to multiple companies (e.g. consultants).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    full_name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Preferences
    preferred_language = models.CharField(max_length=10, default="en")
    timezone = models.CharField(max_length=50, default="Africa/Accra")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Membership(models.Model):
    """
    Links a User to a Company with a specific role.
    This is the multi-tenancy join table.
    """

    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        ADMIN = "admin", "Admin"
        MANAGER = "manager", "Manager"
        TELLER = "teller", "Teller"

    ROLE_HIERARCHY = {
        "owner": 4,
        "admin": 3,
        "manager": 2,
        "teller": 1,
    }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    company = models.ForeignKey(
        "core.Company", on_delete=models.CASCADE, related_name="members"
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.TELLER)
    branch = models.ForeignKey(
        "core.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="staff",
    )

    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    deactivated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [["user", "company"]]
        ordering = ["-joined_at"]

    def __str__(self):
        return f"{self.user.full_name} - {self.role} at {self.company.name}"

    @property
    def role_level(self):
        return self.ROLE_HIERARCHY.get(self.role, 0)

    def has_higher_role_than(self, other_membership):
        return self.role_level > other_membership.role_level


class Invitation(models.Model):
    """Invitations sent by company admins to new users."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        EXPIRED = "expired", "Expired"
        REVOKED = "revoked", "Revoked"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        "core.Company", on_delete=models.CASCADE, related_name="invitations"
    )
    email = models.EmailField()
    role = models.CharField(
        max_length=20,
        choices=Membership.Role.choices,
        default=Membership.Role.TELLER,
    )
    branch = models.ForeignKey(
        "core.Branch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    token = models.CharField(max_length=64, unique=True, default=secrets.token_urlsafe)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    invited_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="sent_invitations"
    )
    expires_at = models.DateTimeField()
    accepted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Invite {self.email} as {self.role} to {self.company.name}"

    @property
    def is_expired(self):
        return self.expires_at < timezone.now()

    @property
    def is_valid(self):
        return self.status == self.Status.PENDING and not self.is_expired


class UserProfile(models.Model):
    """Extended profile info for a user."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    date_of_birth = models.DateField(null=True, blank=True)
    national_id = models.CharField(max_length=50, blank=True)
    id_type = models.CharField(
        max_length=30,
        choices=[
            ("passport", "Passport"),
            ("national_id", "National ID"),
            ("drivers_license", "Driver's License"),
            ("voter_id", "Voter ID"),
        ],
        blank=True,
    )
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"Profile: {self.user.full_name}"
