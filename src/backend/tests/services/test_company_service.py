"""Tests for company service."""

from math import ceil
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from backend.schemas.company import CompanyRead
from backend.services.company_service import get_companies


@pytest.mark.asyncio
async def test_get_companies_delegating_to_repository(
    sample_companies_raw: list[dict[str, Any]],
) -> None:
    """Test that get_companies delegates to repository correctly."""
    # Setup
    mock_client = AsyncMock()

    with (
        patch("backend.services.company_service.company_repository.get_all") as mock_get_all,
        patch("backend.services.company_service.company_repository.count") as mock_count,
    ):
        mock_get_all.return_value = sample_companies_raw
        mock_count.return_value = len(sample_companies_raw)

        # Act
        result = await get_companies(mock_client, page=1, size=20)

        # Assert
        mock_get_all.assert_called_once()
        mock_count.assert_called_once()
        assert len(result.items) == len(sample_companies_raw)


@pytest.mark.asyncio
async def test_get_companies_pagination_metadata(
    sample_companies_raw: list[dict[str, Any]],
) -> None:
    """Test that pagination metadata is calculated correctly."""
    # Setup
    mock_client = AsyncMock()
    total_companies = 100
    page_size = 20

    with (
        patch("backend.services.company_service.company_repository.get_all") as mock_get_all,
        patch("backend.services.company_service.company_repository.count") as mock_count,
    ):
        mock_get_all.return_value = sample_companies_raw
        mock_count.return_value = total_companies

        # Act
        result = await get_companies(mock_client, page=1, size=page_size)

        # Assert
        assert result.total == total_companies
        assert result.page == 1
        assert result.size == page_size
        assert result.total_pages == ceil(total_companies / page_size)


@pytest.mark.asyncio
async def test_get_companies_with_zero_total(
    sample_companies_raw: list[dict[str, Any]],
) -> None:
    """Test that response is valid when total is 0."""
    # Setup
    mock_client = AsyncMock()

    with (
        patch("backend.services.company_service.company_repository.get_all") as mock_get_all,
        patch("backend.services.company_service.company_repository.count") as mock_count,
    ):
        mock_get_all.return_value = []
        mock_count.return_value = 0

        # Act
        result = await get_companies(mock_client, page=1, size=20)

        # Assert
        assert result.items == []
        assert result.total == 0
        assert result.total_pages == 0


@pytest.mark.asyncio
async def test_get_companies_filters_passed_to_repository() -> None:
    """Test that filter parameters are passed correctly to repository."""
    # Setup
    mock_client = AsyncMock()
    industry_id = 1
    location_id = 2
    page = 2
    size = 50

    with (
        patch("backend.services.company_service.company_repository.get_all") as mock_get_all,
        patch("backend.services.company_service.company_repository.count") as mock_count,
    ):
        mock_get_all.return_value = []
        mock_count.return_value = 0

        # Act
        await get_companies(
            mock_client,
            industry_id=industry_id,
            location_id=location_id,
            page=page,
            size=size,
        )

        # Assert
        # Verify parameters passed to get_all
        get_all_call = mock_get_all.call_args
        assert get_all_call.kwargs.get("industry_id") == industry_id
        assert get_all_call.kwargs.get("location_id") == location_id
        assert get_all_call.kwargs.get("page") == page
        assert get_all_call.kwargs.get("size") == size

        # Verify filters passed to count
        count_call = mock_count.call_args
        assert count_call.kwargs.get("industry_id") == industry_id
        assert count_call.kwargs.get("location_id") == location_id


@pytest.mark.asyncio
async def test_get_companies_transforms_to_schema(
    sample_companies_raw: list[dict[str, Any]],
) -> None:
    """Test that raw company data is transformed to CompanyRead schema."""
    # Setup
    mock_client = AsyncMock()

    with (
        patch("backend.services.company_service.company_repository.get_all") as mock_get_all,
        patch("backend.services.company_service.company_repository.count") as mock_count,
    ):
        mock_get_all.return_value = sample_companies_raw
        mock_count.return_value = len(sample_companies_raw)

        # Act
        result = await get_companies(mock_client)

        # Assert
        assert len(result.items) == len(sample_companies_raw)
        for item in result.items:
            assert isinstance(item, CompanyRead)
            assert hasattr(item, "id")
            assert hasattr(item, "name")
            assert hasattr(item, "industry")
            assert hasattr(item, "location")
