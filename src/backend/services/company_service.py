"""Service layer for company business logic."""

from math import ceil
from typing import Any

from supabase._async.client import AsyncClient

from backend.repositories import company_repository
from backend.schemas.company import CompanyListResponse, CompanyRead


def _format_location(location_data: dict[str, Any]) -> str:
    """Format location dict into a readable string.

    Args:
        location_data: Dictionary with city, state, and country fields.

    Returns:
        Formatted string like "City, Country" or "City, State, Country".
    """
    city = location_data.get("city", "")
    state = location_data.get("state")
    country = location_data.get("country", "")

    if state:
        return f"{city}, {state}, {country}"
    return f"{city}, {country}"


def _to_company_read(raw: dict[str, Any]) -> CompanyRead:
    """Transform a raw company dict with embedded relations to CompanyRead.

    Args:
        raw: Raw company record from Supabase with embedded industry and location.

    Returns:
        Validated CompanyRead schema instance.
    """
    industry_name = ""
    if raw.get("industry") and isinstance(raw["industry"], dict):
        industry_name = raw["industry"].get("name", "")

    location_str = ""
    if raw.get("location") and isinstance(raw["location"], dict):
        location_str = _format_location(raw["location"])

    return CompanyRead(
        id=raw["id"],
        name=raw["name"],
        industry=industry_name,
        location=location_str,
        products=raw.get("products", ""),
        founding_year=raw.get("founding_year"),
        total_funding=raw.get("total_funding"),
        arr=raw.get("arr"),
        valuation=raw.get("valuation"),
    )


async def get_companies(
    client: AsyncClient,
    *,
    industry_id: int | None = None,
    location_id: int | None = None,
    page: int = 1,
    size: int = 20,
) -> CompanyListResponse:
    """Fetch paginated companies with optional filters.

    Args:
        client: Async Supabase client instance.
        industry_id: Optional industry ID to filter by.
        location_id: Optional location ID to filter by.
        page: Page number (1-based).
        size: Number of items per page.

    Returns:
        Paginated response with company items and metadata.
    """
    raw_data = await company_repository.get_all(
        client,
        industry_id=industry_id,
        location_id=location_id,
        page=page,
        size=size,
    )

    total = await company_repository.count(
        client,
        industry_id=industry_id,
        location_id=location_id,
    )

    total_pages = ceil(total / size) if total > 0 else 0
    items = [_to_company_read(record) for record in raw_data]

    return CompanyListResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        total_pages=total_pages,
    )
