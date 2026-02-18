"""Repository for industry data access via Supabase."""

from typing import Any, cast

from supabase._async.client import AsyncClient


async def get_all(client: AsyncClient) -> list[dict[str, Any]]:
    """Fetch all industries ordered by name.

    Args:
        client: Async Supabase client instance.

    Returns:
        List of industry records as dictionaries.
    """
    response = await client.table("industry").select("*").order("name").execute()
    return cast(list[dict[str, Any]], response.data)
