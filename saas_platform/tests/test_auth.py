"""
Tests for authentication, login, logout, and team management.
"""

import pytest
from rest_framework import status


@pytest.mark.django_db
class TestLogin:
    def test_login_success(self, api_client, owner_user, owner_membership):
        response = api_client.post("/api/v1/auth/login/", {
            "email": "owner@testcompany.com",
            "password": "securepassword123",
        })
        assert response.status_code == status.HTTP_200_OK
        assert "token" in response.data
        assert response.data["user"]["email"] == "owner@testcompany.com"
        assert response.data["membership"]["role"] == "owner"

    def test_login_wrong_password(self, api_client, owner_user, owner_membership):
        response = api_client.post("/api/v1/auth/login/", {
            "email": "owner@testcompany.com",
            "password": "wrongpassword",
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, api_client):
        response = api_client.post("/api/v1/auth/login/", {
            "email": "nobody@example.com",
            "password": "password123",
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_inactive_user(self, api_client, owner_user, owner_membership):
        owner_user.is_active = False
        owner_user.save()
        response = api_client.post("/api/v1/auth/login/", {
            "email": "owner@testcompany.com",
            "password": "securepassword123",
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestLogout:
    def test_logout_clears_token(self, owner_client, owner_membership):
        response = owner_client.post("/api/v1/auth/logout/")
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCurrentUser:
    def test_me_returns_user_info(self, owner_client, owner_membership):
        response = owner_client.get("/api/v1/auth/me/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["user"]["email"] == "owner@testcompany.com"

    def test_me_requires_auth(self, api_client):
        response = api_client.get("/api/v1/auth/me/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestChangePassword:
    def test_change_password_success(self, owner_client, owner_membership):
        response = owner_client.post("/api/v1/auth/me/password/", {
            "current_password": "securepassword123",
            "new_password": "newsecurepass456",
        })
        assert response.status_code == status.HTTP_200_OK
        assert "token" in response.data  # New token issued

    def test_change_password_wrong_current(self, owner_client, owner_membership):
        response = owner_client.post("/api/v1/auth/me/password/", {
            "current_password": "wrongcurrent",
            "new_password": "newsecurepass456",
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestTeamManagement:
    def test_list_team_members(self, owner_client, owner_membership, teller_membership):
        response = owner_client.get("/api/v1/auth/team/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_teller_cannot_deactivate(self, teller_client, teller_membership, owner_membership):
        response = teller_client.post(
            f"/api/v1/auth/team/{owner_membership.id}/deactivate/"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_owner_can_deactivate_teller(self, owner_client, owner_membership, teller_membership):
        response = owner_client.post(
            f"/api/v1/auth/team/{teller_membership.id}/deactivate/"
        )
        assert response.status_code == status.HTTP_200_OK
