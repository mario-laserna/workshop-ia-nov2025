"""Repository for location data access via Supabase."""

from typing import Any, cast

from supabase._async.client import AsyncClient


async def get_all(client: AsyncClient) -> list[dict[str, Any]]:
    """Fetch all locations ordered by city.

    Args:
        client: Async Supabase client instance.

    Returns:
        List of location records as dictionaries.
    """
    response = await client.table("location").select("*").order("city").execute()
    return cast(list[dict[str, Any]], response.data)
