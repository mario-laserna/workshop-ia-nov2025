"""Tests for locations API endpoints."""

from typing import Any
from unittest.mock import patch

from fastapi.testclient import TestClient


def test_list_locations_returns_200(
    test_client: TestClient, sample_locations: list[dict[str, Any]]
) -> None:
    """Test that GET /api/v1/locations returns 200 with list of locations."""
    # Setup: mock repository to return test data
    with patch("backend.services.location_service.location_repository.get_all") as mock_get_all:
        mock_get_all.return_value = sample_locations

        # Act
        response = test_client.get("/api/v1/locations")

        # Assert
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0
        assert all(
            "id" in item and "city" in item and "country" in item for item in response.json()
        )


def test_list_locations_empty_list(test_client: TestClient) -> None:
    """Test that GET /api/v1/locations returns 200 with empty list when no locations exist."""
    # Setup: mock repository to return empty list
    with patch("backend.services.location_service.location_repository.get_all") as mock_get_all:
        mock_get_all.return_value = []

        # Act
        response = test_client.get("/api/v1/locations")

        # Assert
        assert response.status_code == 200
        assert response.json() == []


def test_list_locations_response_format(
    test_client: TestClient, sample_location: dict[str, Any]
) -> None:
    """Test that locations response has correct format with id, city, state, country."""
    # Setup
    with patch("backend.services.location_service.location_repository.get_all") as mock_get_all:
        mock_get_all.return_value = [sample_location]

        # Act
        response = test_client.get("/api/v1/locations")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == sample_location["id"]
        assert data[0]["city"] == sample_location["city"]
        assert data[0]["country"] == sample_location["country"]
