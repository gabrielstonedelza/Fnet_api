from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Membership, Invitation, UserProfile
from .two_factor import TwoFactorAuth


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["email", "full_name", "phone", "is_active", "is_staff", "created_at"]
    list_filter = ["is_active", "is_staff"]
    search_fields = ["email", "full_name", "phone"]
    ordering = ["-created_at"]
    readonly_fields = ["id", "created_at", "updated_at", "last_login_ip"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("full_name", "phone", "avatar")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Preferences", {"fields": ("preferred_language", "timezone")}),
        ("Metadata", {"fields": ("id", "created_at", "updated_at", "last_login_ip")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "phone", "password1", "password2"),
        }),
    )


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "company", "role", "branch", "is_active", "joined_at"]
    list_filter = ["role", "is_active"]
    search_fields = ["user__full_name", "user__email", "company__name"]
    raw_id_fields = ["user", "company", "branch"]


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ["email", "company", "role", "status", "invited_by", "expires_at"]
    list_filter = ["status", "role"]
    search_fields = ["email", "company__name"]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "national_id", "id_type"]
    search_fields = ["user__full_name", "user__email"]


@admin.register(TwoFactorAuth)
class TwoFactorAuthAdmin(admin.ModelAdmin):
    list_display = ["user", "is_enabled", "is_verified", "created_at"]
    list_filter = ["is_enabled", "is_verified"]
    search_fields = ["user__email", "user__full_name"]
    readonly_fields = ["id", "secret", "backup_codes", "created_at", "updated_at"]
