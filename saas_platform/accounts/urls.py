from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # Auth
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),

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
