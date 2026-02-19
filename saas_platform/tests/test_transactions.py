"""
Tests for transaction creation, approval workflow, and reversals.
"""

import pytest
from decimal import Decimal
from rest_framework import status

from transactions.models import Transaction


@pytest.mark.django_db
class TestCreateTransactions:
    def test_create_bank_deposit(self, owner_client, owner_membership, company_settings, customer):
        response = owner_client.post("/api/v1/transactions/bank-deposit/", {
            "customer": str(customer.id),
            "amount": "500.00",
            "bank_name": "Ecobank",
            "account_number": "1234567890",
            "account_name": "John Doe",
            "depositor_name": "John Doe",
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["transaction_type"] == "deposit"
        assert response.data["channel"] == "bank"
        # 500 < 1000 threshold, so should auto-complete
        assert response.data["status"] == "completed"
        # Fee should be 1% of 500 = 5.00
        assert Decimal(response.data["fee"]) == Decimal("5.00")

    def test_large_deposit_requires_approval(self, owner_client, owner_membership, company_settings, customer):
        response = owner_client.post("/api/v1/transactions/bank-deposit/", {
            "customer": str(customer.id),
            "amount": "5000.00",
            "bank_name": "GCB",
            "account_number": "9876543210",
            "account_name": "John Doe",
            "depositor_name": "John Doe",
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["status"] == "pending"
        assert response.data["requires_approval"] is True

    def test_create_cash_transaction(self, owner_client, owner_membership, company_settings, customer):
        response = owner_client.post("/api/v1/transactions/cash/", {
            "customer": str(customer.id),
            "transaction_type": "deposit",
            "amount": "200.00",
            "d_100": 2,
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["channel"] == "cash"

    def test_create_momo_transaction(self, owner_client, owner_membership, company_settings, customer):
        response = owner_client.post("/api/v1/transactions/mobile-money/", {
            "customer": str(customer.id),
            "transaction_type": "deposit",
            "amount": "100.00",
            "network": "mtn",
            "service_type": "cash_in",
            "sender_number": "+233501234567",
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["channel"] == "mobile_money"


@pytest.mark.django_db
class TestApprovalWorkflow:
    def test_approve_transaction(
        self, owner_client, teller_client, owner_membership, teller_membership, company_settings, customer
    ):
        # Teller creates a large transaction
        create_resp = teller_client.post("/api/v1/transactions/bank-deposit/", {
            "customer": str(customer.id),
            "amount": "5000.00",
            "bank_name": "Ecobank",
            "account_number": "1234567890",
            "account_name": "John Doe",
            "depositor_name": "John Doe",
        })
        assert create_resp.status_code == status.HTTP_201_CREATED
        tx_id = create_resp.data["id"]

        # Owner approves it
        approve_resp = owner_client.post(f"/api/v1/transactions/{tx_id}/approve/", {
            "action": "approve",
        })
        assert approve_resp.status_code == status.HTTP_200_OK
        assert approve_resp.data["status"] == "completed"

    def test_cannot_approve_own_transaction(
        self, owner_client, owner_membership, company_settings, customer
    ):
        create_resp = owner_client.post("/api/v1/transactions/bank-deposit/", {
            "customer": str(customer.id),
            "amount": "5000.00",
            "bank_name": "GCB",
            "account_number": "1234567890",
            "account_name": "Self",
            "depositor_name": "Self",
        })
        tx_id = create_resp.data["id"]

        approve_resp = owner_client.post(f"/api/v1/transactions/{tx_id}/approve/", {
            "action": "approve",
        })
        assert approve_resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_teller_cannot_approve(
        self, owner_client, teller_client, owner_membership, teller_membership, company_settings, customer
    ):
        create_resp = owner_client.post("/api/v1/transactions/bank-deposit/", {
            "customer": str(customer.id),
            "amount": "5000.00",
            "bank_name": "GCB",
            "account_number": "1234567890",
            "account_name": "Test",
            "depositor_name": "Test",
        })
        tx_id = create_resp.data["id"]

        approve_resp = teller_client.post(f"/api/v1/transactions/{tx_id}/approve/", {
            "action": "approve",
        })
        assert approve_resp.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestReversal:
    def test_reverse_completed_transaction(
        self, owner_client, owner_membership, company_settings, customer
    ):
        # Create a small (auto-complete) transaction
        create_resp = owner_client.post("/api/v1/transactions/bank-deposit/", {
            "customer": str(customer.id),
            "amount": "200.00",
            "bank_name": "Ecobank",
            "account_number": "1234567890",
            "account_name": "John Doe",
            "depositor_name": "John Doe",
        })
        tx_id = create_resp.data["id"]

        reverse_resp = owner_client.post(f"/api/v1/transactions/{tx_id}/reverse/", {
            "reason": "Customer request",
        })
        assert reverse_resp.status_code == status.HTTP_201_CREATED
        assert reverse_resp.data["transaction_type"] == "reversal"

    def test_teller_cannot_reverse(
        self, owner_client, teller_client, owner_membership, teller_membership, company_settings, customer
    ):
        create_resp = owner_client.post("/api/v1/transactions/bank-deposit/", {
            "customer": str(customer.id),
            "amount": "200.00",
            "bank_name": "GCB",
            "account_number": "1234567890",
            "account_name": "Test",
            "depositor_name": "Test",
        })
        tx_id = create_resp.data["id"]

        reverse_resp = teller_client.post(f"/api/v1/transactions/{tx_id}/reverse/", {
            "reason": "Teller trying",
        })
        assert reverse_resp.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestTransactionList:
    def test_owner_sees_all_transactions(
        self, owner_client, teller_client, owner_membership, teller_membership, company_settings, customer
    ):
        # Teller creates 2 transactions
        for _ in range(2):
            teller_client.post("/api/v1/transactions/cash/", {
                "customer": str(customer.id),
                "transaction_type": "deposit",
                "amount": "100.00",
            })

        response = owner_client.get("/api/v1/transactions/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_teller_sees_only_own_transactions(
        self, owner_client, teller_client, owner_membership, teller_membership, company_settings, customer
    ):
        # Owner creates 1 transaction
        owner_client.post("/api/v1/transactions/cash/", {
            "customer": str(customer.id),
            "transaction_type": "deposit",
            "amount": "100.00",
        })
        # Teller creates 1 transaction
        teller_client.post("/api/v1/transactions/cash/", {
            "customer": str(customer.id),
            "transaction_type": "deposit",
            "amount": "100.00",
        })

        response = teller_client.get("/api/v1/transactions/")
        assert response.status_code == status.HTTP_200_OK
        # Teller should only see their own
        assert len(response.data) == 1
