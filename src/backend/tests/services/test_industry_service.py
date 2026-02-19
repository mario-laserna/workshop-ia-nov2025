"""Tests for industry service."""

from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from backend.schemas.industry import IndustryRead
from backend.services.industry_service import get_all_industries


@pytest.mark.asyncio
async def test_get_all_industries_delegating_to_repository(
    sample_industries: list[dict[str, Any]],
) -> None:
    """Test that get_all_industries delegates to repository correctly."""
    # Setup
    mock_client = AsyncMock()

    with patch("backend.services.industry_service.industry_repository.get_all") as mock_get_all:
        mock_get_all.return_value = sample_industries

        # Act
        result = await get_all_industries(mock_client)

        # Assert
        mock_get_all.assert_called_once()
        assert len(result) == len(sample_industries)


@pytest.mark.asyncio
async def test_get_all_industries_with_empty_list() -> None:
    """Test that empty list is handled correctly."""
    # Setup
    mock_client = AsyncMock()

    with patch("backend.services.industry_service.industry_repository.get_all") as mock_get_all:
        mock_get_all.return_value = []

        # Act
        result = await get_all_industries(mock_client)

        # Assert
        assert result == []


@pytest.mark.asyncio
async def test_get_all_industries_transforms_to_schema(
    sample_industries: list[dict[str, Any]],
) -> None:
    """Test that raw industry data is transformed to IndustryRead schema."""
    # Setup
    mock_client = AsyncMock()

    with patch("backend.services.industry_service.industry_repository.get_all") as mock_get_all:
        mock_get_all.return_value = sample_industries

        # Act
        result = await get_all_industries(mock_client)

        # Assert
        assert len(result) == len(sample_industries)
        for item in result:
            assert isinstance(item, IndustryRead)
            assert hasattr(item, "id")
            assert hasattr(item, "name")
