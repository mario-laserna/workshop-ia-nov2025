"""Pytest configuration and shared fixtures for backend tests."""

from typing import Any, AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient
from supabase._async.client import AsyncClient

from backend.core.supabase_client import get_supabase
from backend.main import app

# ============================================================================
# Test Data Fixtures
# ============================================================================


@pytest.fixture
def sample_industry() -> dict[str, Any]:
    """Sample industry record for testing."""
    return {
        "id": 1,
        "name": "SaaS",
    }


@pytest.fixture
def sample_industries(sample_industry: dict[str, Any]) -> list[dict[str, Any]]:
    """Sample list of industries for testing."""
    return [
        sample_industry,
        {"id": 2, "name": "FinTech"},
        {"id": 3, "name": "HRTech"},
    ]


@pytest.fixture
def sample_location() -> dict[str, Any]:
    """Sample location record for testing."""
    return {
        "id": 1,
        "city": "San Francisco",
        "state": "CA",
        "country": "USA",
    }


@pytest.fixture
def sample_locations(sample_location: dict[str, Any]) -> list[dict[str, Any]]:
    """Sample list of locations for testing."""
    return [
        sample_location,
        {"id": 2, "city": "New York", "state": "NY", "country": "USA"},
        {"id": 3, "city": "London", "state": None, "country": "UK"},
    ]


@pytest.fixture
def sample_company_raw() -> dict[str, Any]:
    """Raw company record as returned by Supabase with embedded relations."""
    return {
        "id": 1,
        "name": "Figma",
        "products": "Design collaboration tool",
        "founding_year": 2012,
        "total_funding": 200000000,
        "arr": 150000000,
        "valuation": 10000000000,
        "industry_id": 1,
        "location_id": 1,
        "industry": {"name": "SaaS"},
        "location": {
            "city": "San Francisco",
            "state": "CA",
            "country": "USA",
        },
        "created_at": "2024-01-01T00:00:00Z",
        "created_by": "admin",
        "updated_at": "2024-01-01T00:00:00Z",
        "updated_by": "admin",
    }


@pytest.fixture
def sample_companies_raw(sample_company_raw: dict[str, Any]) -> list[dict[str, Any]]:
    """Sample list of raw company records for testing."""
    return [
        sample_company_raw,
        {
            "id": 2,
            "name": "Stripe",
            "products": "Payment processing",
            "founding_year": 2010,
            "total_funding": 650000000,
            "arr": 500000000,
            "valuation": 95000000000,
            "industry_id": 2,
            "location_id": 1,
            "industry": {"name": "FinTech"},
            "location": {
                "city": "San Francisco",
                "state": "CA",
                "country": "USA",
            },
            "created_at": "2024-01-01T00:00:00Z",
            "created_by": "admin",
            "updated_at": "2024-01-01T00:00:00Z",
            "updated_by": "admin",
        },
    ]


# ============================================================================
# Mock Supabase Client Fixtures
# ============================================================================


@pytest.fixture
async def mock_supabase_client() -> AsyncMock:
    """Create a mock async Supabase client for testing.

    Returns:
        AsyncMock: Mocked AsyncClient instance.
    """
    return AsyncMock(spec=AsyncClient)


@pytest.fixture
def supabase_override(
    mock_supabase_client: AsyncMock,
) -> Any:
    """Override the get_supabase dependency in FastAPI.

    Args:
        mock_supabase_client: The mocked AsyncClient.

    Yields:
        AsyncMock: Mocked AsyncClient for dependency injection.
    """

    async def _get_supabase() -> AsyncGenerator[AsyncMock, None]:
        yield mock_supabase_client

    return _get_supabase


# ============================================================================
# TestClient Fixtures
# ============================================================================


@pytest.fixture
def test_client(mock_supabase_client: AsyncMock) -> TestClient:  # type: ignore[misc]
    """Create a FastAPI TestClient with mock Supabase dependency.

    Args:
        mock_supabase_client: The mocked AsyncClient.

    Yields:
        TestClient: FastAPI test client with mocked dependencies.
    """

    async def _override_get_supabase() -> AsyncGenerator[AsyncMock, None]:
        yield mock_supabase_client

    app.dependency_overrides[get_supabase] = _override_get_supabase
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# ============================================================================
# Helper Functions for Mocking Supabase Responses
# ============================================================================


def mock_supabase_response(data: Any, count: int | None = None) -> MagicMock:
    """Create a mock Supabase response object.

    Args:
        data: The data to return in the response.
        count: Optional count for pagination responses.

    Returns:
        MagicMock: Mocked response object.
    """
    response = MagicMock()
    response.data = data
    response.count = count
    return response


@pytest.fixture
def mock_supabase_table_query() -> MagicMock:
    """Create a chainable mock for Supabase table query builder.

    Returns:
        MagicMock: Mocked table query builder.
    """
    query = MagicMock()
    query.select = MagicMock(return_value=query)
    query.eq = MagicMock(return_value=query)
    query.range = MagicMock(return_value=query)
    query.order = MagicMock(return_value=query)
    query.execute = AsyncMock()
    return query
