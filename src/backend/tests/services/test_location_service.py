"""Tests for location service."""

from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from backend.schemas.location import LocationRead
from backend.services.location_service import get_all_locations


@pytest.mark.asyncio
async def test_get_all_locations_delegating_to_repository(
    sample_locations: list[dict[str, Any]],
) -> None:
    """Test that get_all_locations delegates to repository correctly."""
    # Setup
    mock_client = AsyncMock()

    with patch("backend.services.location_service.location_repository.get_all") as mock_get_all:
        mock_get_all.return_value = sample_locations

        # Act
        result = await get_all_locations(mock_client)

        # Assert
        mock_get_all.assert_called_once()
        assert len(result) == len(sample_locations)


@pytest.mark.asyncio
async def test_get_all_locations_with_empty_list() -> None:
    """Test that empty list is handled correctly."""
    # Setup
    mock_client = AsyncMock()

    with patch("backend.services.location_service.location_repository.get_all") as mock_get_all:
        mock_get_all.return_value = []

        # Act
        result = await get_all_locations(mock_client)

        # Assert
        assert result == []


@pytest.mark.asyncio
async def test_get_all_locations_transforms_to_schema(
    sample_locations: list[dict[str, Any]],
) -> None:
    """Test that raw location data is transformed to LocationRead schema."""
    # Setup
    mock_client = AsyncMock()

    with patch("backend.services.location_service.location_repository.get_all") as mock_get_all:
        mock_get_all.return_value = sample_locations

        # Act
        result = await get_all_locations(mock_client)

        # Assert
        assert len(result) == len(sample_locations)
        for item in result:
            assert isinstance(item, LocationRead)
            assert hasattr(item, "id")
            assert hasattr(item, "city")
            assert hasattr(item, "country")
