"""Service layer for location business logic."""

from supabase._async.client import AsyncClient

from backend.repositories import location_repository
from backend.schemas.location import LocationRead


async def get_all_locations(client: AsyncClient) -> list[LocationRead]:
    """Fetch all locations and return as validated schemas.

    Args:
        client: Async Supabase client instance.

    Returns:
        List of LocationRead schemas.
    """
    raw_data = await location_repository.get_all(client)
    return [LocationRead(**item) for item in raw_data]
