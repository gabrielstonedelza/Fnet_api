"""
Tests for role-based access control and permission boundaries.
"""

import pytest
from rest_framework import status


@pytest.mark.django_db
class TestRoleBasedAccess:
    """Ensure each endpoint respects role hierarchy."""

    def test_teller_cannot_access_reports(self, teller_client, teller_membership):
        response = teller_client.get("/api/v1/reports/dashboard/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_owner_can_access_reports(self, owner_client, owner_membership):
        response = owner_client.get("/api/v1/reports/dashboard/")
        assert response.status_code == status.HTTP_200_OK

    def test_teller_cannot_manage_team(self, teller_client, teller_membership, owner_membership):
        response = teller_client.post(
            f"/api/v1/auth/team/{owner_membership.id}/deactivate/"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_teller_cannot_access_audit(self, teller_client, teller_membership):
        response = teller_client.get("/api/v1/audit/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_teller_cannot_approve_pending(self, teller_client, teller_membership):
        response = teller_client.get("/api/v1/transactions/pending/")
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestUnauthenticatedAccess:
    """Ensure endpoints require authentication."""

    def test_transactions_require_auth(self, api_client):
        response = api_client.get("/api/v1/transactions/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_customers_require_auth(self, api_client):
        response = api_client.get("/api/v1/customers/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_notifications_require_auth(self, api_client):
        response = api_client.get("/api/v1/notifications/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_health_check_is_public(self, api_client):
        response = api_client.get("/api/v1/health/")
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestTenantIsolation:
    """Ensure companies can't see each other's data."""

    def test_cannot_see_other_company_customers(
        self, api_client, pro_plan, owner_user, db
    ):
        from core.models import Company, CompanySettings
        from accounts.models import Membership, User
        from customers.models import Customer
        from rest_framework.authtoken.models import Token

        # Create company A
        company_a = Company.objects.create(
            name="Company A", slug="company-a", email="a@a.com",
            phone="+233100000000", subscription_plan=pro_plan,
            subscription_status="active", status="active",
        )
        user_a = User.objects.create_user(
            email="usera@a.com", password="pass123", full_name="User A",
        )
        Membership.objects.create(user=user_a, company=company_a, role="owner", is_active=True)
        Customer.objects.create(
            company=company_a, full_name="Company A Customer",
            phone="+233111111111", registered_by=user_a,
        )

        # Create company B
        company_b = Company.objects.create(
            name="Company B", slug="company-b", email="b@b.com",
            phone="+233200000000", subscription_plan=pro_plan,
            subscription_status="active", status="active",
        )
        user_b = User.objects.create_user(
            email="userb@b.com", password="pass123", full_name="User B",
        )
        Membership.objects.create(user=user_b, company=company_b, role="owner", is_active=True)

        # User B requests customers — should get 0, not Company A's customer
        token_b, _ = Token.objects.get_or_create(user=user_b)
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {token_b.key}")
        api_client.defaults["HTTP_X_COMPANY_ID"] = str(company_b.id)

        response = api_client.get("/api/v1/customers/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0
