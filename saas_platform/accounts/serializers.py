from rest_framework import serializers
from .models import User, Membership, Invitation, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "email", "phone", "full_name", "avatar",
            "preferred_language", "timezone",
            "is_active", "created_at", "last_login_ip",
        ]
        read_only_fields = ["id", "created_at", "last_login_ip"]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone", "full_name", "avatar", "preferred_language", "timezone"]


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(min_length=8, write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "date_of_birth", "national_id", "id_type",
            "emergency_contact_name", "emergency_contact_phone", "address",
        ]


class MembershipSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_full_name = serializers.CharField(source="user.full_name", read_only=True)
    user_phone = serializers.CharField(source="user.phone", read_only=True)
    user_avatar = serializers.ImageField(source="user.avatar", read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)
    branch_name = serializers.CharField(source="branch.name", read_only=True, default=None)

    class Meta:
        model = Membership
        fields = [
            "id", "user", "user_email", "user_full_name", "user_phone", "user_avatar",
            "company", "company_name",
            "role", "branch", "branch_name",
            "is_active", "joined_at", "deactivated_at",
        ]
        read_only_fields = ["id", "user", "company", "joined_at", "deactivated_at"]


class InvitationCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=Membership.Role.choices)
    branch = serializers.UUIDField(required=False, allow_null=True)


class InvitationSerializer(serializers.ModelSerializer):
    invited_by_name = serializers.CharField(
        source="invited_by.full_name", read_only=True
    )
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = Invitation
        fields = [
            "id", "company", "company_name", "email", "role",
            "branch", "token", "status",
            "invited_by", "invited_by_name",
            "expires_at", "accepted_at", "created_at",
        ]
        read_only_fields = [
            "id", "company", "token", "status",
            "invited_by", "expires_at", "accepted_at", "created_at",
        ]


class AcceptInvitationSerializer(serializers.Serializer):
    token = serializers.CharField()
    full_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=20, required=False)
    password = serializers.CharField(min_length=8, write_only=True)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    company_id = serializers.UUIDField(
        required=False,
        help_text="Required if user belongs to multiple companies.",
    )
