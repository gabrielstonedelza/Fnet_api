"""
Tests for health check endpoints.
"""

import pytest
from rest_framework import status


@pytest.mark.django_db
class TestHealthCheck:
    def test_liveness_probe(self, api_client):
        response = api_client.get("/api/v1/health/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "healthy"

    def test_readiness_probe(self, api_client):
        response = api_client.get("/api/v1/health/ready/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["checks"]["database"] == "ok"
