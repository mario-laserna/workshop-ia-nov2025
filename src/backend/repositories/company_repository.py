"""Repository for company data access via Supabase."""

from typing import Any, cast

from supabase._async.client import AsyncClient

COMPANY_SELECT = "*, industry(name), location(city, state, country)"
"""Select query with embedded relations for company table."""


async def get_all(
    client: AsyncClient,
    *,
    industry_id: int | None = None,
    location_id: int | None = None,
    page: int = 1,
    size: int = 20,
) -> list[dict[str, Any]]:
    """Fetch companies with optional filters and pagination.

    Uses PostgREST embedded relations to include industry and location
    data in a single query, avoiding N+1 problems.

    Args:
        client: Async Supabase client instance.
        industry_id: Optional industry ID to filter by.
        location_id: Optional location ID to filter by.
        page: Page number (1-based).
        size: Number of items per page.

    Returns:
        List of company records as dictionaries with embedded relations.
    """
    query = client.table("company").select(COMPANY_SELECT)

    if industry_id is not None:
        query = query.eq("industry_id", industry_id)

    if location_id is not None:
        query = query.eq("location_id", location_id)

    start = (page - 1) * size
    end = start + size - 1

    response = await query.range(start, end).execute()
    return cast(list[dict[str, Any]], response.data)


async def count(
    client: AsyncClient,
    *,
    industry_id: int | None = None,
    location_id: int | None = None,
) -> int:
    """Count companies matching the given filters.

    Args:
        client: Async Supabase client instance.
        industry_id: Optional industry ID to filter by.
        location_id: Optional location ID to filter by.

    Returns:
        Total number of matching companies.
    """
    query = client.table("company").select("*", count="exact", head=True)

    if industry_id is not None:
        query = query.eq("industry_id", industry_id)

    if location_id is not None:
        query = query.eq("location_id", location_id)

    response = await query.execute()
    return response.count or 0
