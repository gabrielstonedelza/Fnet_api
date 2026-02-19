from django.urls import path
from . import views
from . import views_2fa

app_name = "accounts"

urlpatterns = [
    # Auth
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),

    # Two-Factor Authentication
    path("2fa/status/", views_2fa.twofa_status, name="2fa-status"),
    path("2fa/setup/", views_2fa.twofa_setup, name="2fa-setup"),
    path("2fa/verify-setup/", views_2fa.twofa_verify_setup, name="2fa-verify-setup"),
    path("2fa/verify/", views_2fa.twofa_verify_login, name="2fa-verify-login"),
    path("2fa/disable/", views_2fa.twofa_disable, name="2fa-disable"),
    path("2fa/backup-codes/", views_2fa.twofa_regenerate_backup_codes, name="2fa-backup-codes"),

    # Current user
    path("me/", views.me, name="me"),
    path("me/update/", views.update_me, name="update-me"),
    path("me/password/", views.change_password, name="change-password"),
    path("me/profile/", views.user_profile, name="user-profile"),

    # Team
    path("team/", views.team_members, name="team-list"),
    path("team/<uuid:member_id>/", views.team_member_detail, name="team-detail"),
    path("team/<uuid:member_id>/update/", views.update_team_member, name="team-update"),
    path("team/<uuid:member_id>/deactivate/", views.deactivate_team_member, name="team-deactivate"),

    # Invitations
    path("invitations/", views.invitations, name="invitation-list-create"),
    path("invitations/<uuid:invitation_id>/revoke/", views.revoke_invitation, name="invitation-revoke"),
    path("invitations/accept/", views.accept_invitation, name="invitation-accept"),
]
