"""Tests for companies API endpoints."""

from typing import Any
from unittest.mock import patch

from fastapi.testclient import TestClient


def test_list_companies_returns_200(
    test_client: TestClient, sample_companies_raw: list[dict[str, Any]]
) -> None:
    """Test that GET /api/v1/companies returns 200 with paginated companies."""
    # Setup
    with (
        patch("backend.repositories.company_repository.get_all") as mock_get_all,
        patch("backend.repositories.company_repository.count") as mock_count,
    ):
        mock_get_all.return_value = sample_companies_raw
        mock_count.return_value = len(sample_companies_raw)

        # Act
        response = test_client.get("/api/v1/companies")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
        assert "total_pages" in data


def test_list_companies_with_industry_filter(
    test_client: TestClient, sample_companies_raw: list[dict[str, Any]]
) -> None:
    """Test that companies can be filtered by industry_id."""
    # Filter to first company only
    filtered = [sample_companies_raw[0]]

    # Setup
    with (
        patch("backend.repositories.company_repository.get_all") as mock_get_all,
        patch("backend.repositories.company_repository.count") as mock_count,
    ):
        mock_get_all.return_value = filtered
        mock_count.return_value = 1

        # Act
        response = test_client.get("/api/v1/companies?industry_id=1")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1


def test_list_companies_with_location_filter(
    test_client: TestClient, sample_companies_raw: list[dict[str, Any]]
) -> None:
    """Test that companies can be filtered by location_id."""
    # Filter to first company only
    filtered = [sample_companies_raw[0]]

    # Setup
    with (
        patch("backend.repositories.company_repository.get_all") as mock_get_all,
        patch("backend.repositories.company_repository.count") as mock_count,
    ):
        mock_get_all.return_value = filtered
        mock_count.return_value = 1

        # Act
        response = test_client.get("/api/v1/companies?location_id=1")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1


def test_list_companies_with_combined_filters(
    test_client: TestClient, sample_companies_raw: list[dict[str, Any]]
) -> None:
    """Test that companies can be filtered by both industry_id and location_id."""
    # Filter to first company only
    filtered = [sample_companies_raw[0]]

    # Setup
    with (
        patch("backend.repositories.company_repository.get_all") as mock_get_all,
        patch("backend.repositories.company_repository.count") as mock_count,
    ):
        mock_get_all.return_value = filtered
        mock_count.return_value = 1

        # Act
        response = test_client.get("/api/v1/companies?industry_id=1&location_id=1")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1


def test_list_companies_pagination(
    test_client: TestClient, sample_companies_raw: list[dict[str, Any]]
) -> None:
    """Test that pagination parameters work correctly."""
    # Setup - return first company for page 1, size 1
    with (
        patch("backend.repositories.company_repository.get_all") as mock_get_all,
        patch("backend.repositories.company_repository.count") as mock_count,
    ):
        mock_get_all.return_value = [sample_companies_raw[0]]
        mock_count.return_value = len(sample_companies_raw)

        # Act
        response = test_client.get("/api/v1/companies?page=1&size=1")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["size"] == 1
        assert len(data["items"]) <= 1


def test_list_companies_empty_results(
    test_client: TestClient,
) -> None:
    """Test that empty results return valid response with zero items."""
    # Setup - return empty list
    with (
        patch("backend.repositories.company_repository.get_all") as mock_get_all,
        patch("backend.repositories.company_repository.count") as mock_count,
    ):
        mock_get_all.return_value = []
        mock_count.return_value = 0

        # Act
        response = test_client.get("/api/v1/companies?industry_id=999")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0


def test_list_companies_invalid_page(test_client: TestClient) -> None:
    """Test that page=0 returns 422 validation error."""
    # Act
    response = test_client.get("/api/v1/companies?page=0")

    # Assert
    assert response.status_code == 422


def test_list_companies_invalid_size_too_large(test_client: TestClient) -> None:
    """Test that size > 100 returns 422 validation error."""
    # Act
    response = test_client.get("/api/v1/companies?size=200")

    # Assert
    assert response.status_code == 422


def test_list_companies_response_format(
    test_client: TestClient, sample_companies_raw: list[dict[str, Any]]
) -> None:
    """Test that company response has correct fields and formatting."""
    # Setup
    with (
        patch("backend.repositories.company_repository.get_all") as mock_get_all,
        patch("backend.repositories.company_repository.count") as mock_count,
    ):
        mock_get_all.return_value = sample_companies_raw
        mock_count.return_value = len(sample_companies_raw)

        # Act
        response = test_client.get("/api/v1/companies")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) > 0

        company = data["items"][0]
        required_fields = [
            "id",
            "name",
            "industry",
            "location",
            "products",
            "founding_year",
            "total_funding",
            "arr",
            "valuation",
        ]
        for field in required_fields:
            assert field in company
