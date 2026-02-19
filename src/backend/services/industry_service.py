"""Service layer for industry business logic."""

from supabase._async.client import AsyncClient

from backend.repositories import industry_repository
from backend.schemas.industry import IndustryRead


async def get_all_industries(client: AsyncClient) -> list[IndustryRead]:
    """Fetch all industries and return as validated schemas.

    Args:
        client: Async Supabase client instance.

    Returns:
        List of IndustryRead schemas.
    """
    raw_data = await industry_repository.get_all(client)
    return [IndustryRead(**item) for item in raw_data]
