"""Tests for industries API endpoints."""

from typing import Any
from unittest.mock import patch

from fastapi.testclient import TestClient


def test_list_industries_returns_200(
    test_client: TestClient, sample_industries: list[dict[str, Any]]
) -> None:
    """Test that GET /api/v1/industries returns 200 with list of industries."""
    # Setup: mock repository to return test data
    with patch("backend.services.industry_service.industry_repository.get_all") as mock_get_all:
        mock_get_all.return_value = sample_industries

        # Act
        response = test_client.get("/api/v1/industries")

        # Assert
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0
        assert all("id" in item and "name" in item for item in response.json())


def test_list_industries_empty_list(test_client: TestClient) -> None:
    """Test that GET /api/v1/industries returns 200 with empty list when no industries exist."""
    # Setup: mock repository to return empty list
    with patch("backend.services.industry_service.industry_repository.get_all") as mock_get_all:
        mock_get_all.return_value = []

        # Act
        response = test_client.get("/api/v1/industries")

        # Assert
        assert response.status_code == 200
        assert response.json() == []


def test_list_industries_response_format(
    test_client: TestClient, sample_industry: dict[str, Any]
) -> None:
    """Test that industries response has correct format with id and name."""
    # Setup
    with patch("backend.services.industry_service.industry_repository.get_all") as mock_get_all:
        mock_get_all.return_value = [sample_industry]

        # Act
        response = test_client.get("/api/v1/industries")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == sample_industry["id"]
        assert data[0]["name"] == sample_industry["name"]
