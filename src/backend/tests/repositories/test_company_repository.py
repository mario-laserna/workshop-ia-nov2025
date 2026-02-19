"""Tests for company repository."""

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from backend.repositories import company_repository
from backend.tests.conftest import mock_supabase_response


@pytest.mark.asyncio
async def test_get_all_without_filters(
    sample_companies_raw: list[dict[str, Any]],
) -> None:
    """Test that get_all queries without filters builds correct query."""
    # Setup
    mock_client = AsyncMock()
    query = AsyncMock()
    query.select = MagicMock(return_value=query)
    query.range = MagicMock(return_value=query)
    query.execute = AsyncMock(return_value=mock_supabase_response(sample_companies_raw))
    mock_client.table = MagicMock(return_value=query)

    # Act
    result = await company_repository.get_all(mock_client, page=1, size=20)

    # Assert
    assert result == sample_companies_raw
    mock_client.table.assert_called_once_with("company")
    query.select.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_with_industry_filter(
    sample_companies_raw: list[dict[str, Any]],
) -> None:
    """Test that industry_id filter is applied correctly."""
    # Setup
    mock_client = AsyncMock()
    query = AsyncMock()
    query.select = MagicMock(return_value=query)
    query.eq = MagicMock(return_value=query)
    query.range = MagicMock(return_value=query)
    query.execute = AsyncMock(return_value=mock_supabase_response([sample_companies_raw[0]]))
    mock_client.table = MagicMock(return_value=query)

    # Act
    result = await company_repository.get_all(mock_client, industry_id=1, page=1, size=20)

    # Assert
    assert len(result) == 1
    # Verify eq was called with industry_id
    query.eq.assert_any_call("industry_id", 1)


@pytest.mark.asyncio
async def test_get_all_with_location_filter(
    sample_companies_raw: list[dict[str, Any]],
) -> None:
    """Test that location_id filter is applied correctly."""
    # Setup
    mock_client = AsyncMock()
    query = AsyncMock()
    query.select = MagicMock(return_value=query)
    query.eq = MagicMock(return_value=query)
    query.range = MagicMock(return_value=query)
    query.execute = AsyncMock(return_value=mock_supabase_response([sample_companies_raw[0]]))
    mock_client.table = MagicMock(return_value=query)

    # Act
    result = await company_repository.get_all(mock_client, location_id=1, page=1, size=20)

    # Assert
    assert len(result) == 1
    # Verify eq was called with location_id
    query.eq.assert_any_call("location_id", 1)


@pytest.mark.asyncio
async def test_get_all_with_combined_filters(
    sample_companies_raw: list[dict[str, Any]],
) -> None:
    """Test that both filters are applied correctly together."""
    # Setup
    mock_client = AsyncMock()
    query = AsyncMock()
    query.select = MagicMock(return_value=query)
    query.eq = MagicMock(return_value=query)
    query.range = MagicMock(return_value=query)
    query.execute = AsyncMock(return_value=mock_supabase_response([sample_companies_raw[0]]))
    mock_client.table = MagicMock(return_value=query)

    # Act
    result = await company_repository.get_all(
        mock_client, industry_id=1, location_id=1, page=1, size=20
    )

    # Assert
    assert len(result) == 1
    # Verify both eq calls were made
    assert query.eq.call_count == 2


@pytest.mark.asyncio
async def test_get_all_pagination_offset_calculation(
    sample_companies_raw: list[dict[str, Any]],
) -> None:
    """Test that pagination offset is calculated correctly."""
    # Setup
    mock_client = AsyncMock()
    query = AsyncMock()
    query.select = MagicMock(return_value=query)
    query.range = MagicMock(return_value=query)
    query.execute = AsyncMock(return_value=mock_supabase_response(sample_companies_raw))
    mock_client.table = MagicMock(return_value=query)

    # Act - page 2, size 20 should have start=20, end=39
    await company_repository.get_all(mock_client, page=2, size=20)

    # Assert
    query.range.assert_called_once_with(20, 39)


@pytest.mark.asyncio
async def test_count_without_filters() -> None:
    """Test that count query without filters builds correctly."""
    # Setup
    mock_client = AsyncMock()
    query = AsyncMock()
    query.select = MagicMock(return_value=query)
    query.execute = AsyncMock(return_value=mock_supabase_response([], count=100))
    mock_client.table = MagicMock(return_value=query)

    # Act
    result = await company_repository.count(mock_client)

    # Assert
    assert result == 100
    query.select.assert_called_once_with("*", count="exact", head=True)


@pytest.mark.asyncio
async def test_count_with_industry_filter() -> None:
    """Test that count with industry filter applies correctly."""
    # Setup
    mock_client = AsyncMock()
    query = AsyncMock()
    query.select = MagicMock(return_value=query)
    query.eq = MagicMock(return_value=query)
    query.execute = AsyncMock(return_value=mock_supabase_response([], count=50))
    mock_client.table = MagicMock(return_value=query)

    # Act
    result = await company_repository.count(mock_client, industry_id=1)

    # Assert
    assert result == 50
    query.eq.assert_called_once_with("industry_id", 1)


@pytest.mark.asyncio
async def test_count_with_location_filter() -> None:
    """Test that count with location filter applies correctly."""
    # Setup
    mock_client = AsyncMock()
    query = AsyncMock()
    query.select = MagicMock(return_value=query)
    query.eq = MagicMock(return_value=query)
    query.execute = AsyncMock(return_value=mock_supabase_response([], count=30))
    mock_client.table = MagicMock(return_value=query)

    # Act
    result = await company_repository.count(mock_client, location_id=1)

    # Assert
    assert result == 30
    query.eq.assert_called_once_with("location_id", 1)
