"""Tests for location repository."""

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from backend.repositories import location_repository
from backend.tests.conftest import mock_supabase_response


@pytest.mark.asyncio
async def test_get_all_verifies_order(
    sample_locations: list[dict[str, Any]],
) -> None:
    """Test that locations are ordered by city."""
    # Setup
    mock_client = AsyncMock()
    query = AsyncMock()
    query.select = MagicMock(return_value=query)
    query.order = MagicMock(return_value=query)
    query.execute = AsyncMock(return_value=mock_supabase_response(sample_locations))
    mock_client.table = MagicMock(return_value=query)

    # Act
    result = await location_repository.get_all(mock_client)

    # Assert
    assert result == sample_locations
    query.order.assert_called_once_with("city")


@pytest.mark.asyncio
async def test_get_all_empty_list() -> None:
    """Test that empty list is returned correctly."""
    # Setup
    mock_client = AsyncMock()
    query = AsyncMock()
    query.select = MagicMock(return_value=query)
    query.order = MagicMock(return_value=query)
    query.execute = AsyncMock(return_value=mock_supabase_response([]))
    mock_client.table = MagicMock(return_value=query)

    # Act
    result = await location_repository.get_all(mock_client)

    # Assert
    assert result == []
