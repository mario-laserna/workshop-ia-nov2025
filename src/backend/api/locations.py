"""Router for location endpoints."""

from fastapi import APIRouter, Depends
from supabase._async.client import AsyncClient

from backend.core.settings import settings
from backend.core.supabase_client import get_supabase
from backend.schemas.location import LocationRead
from backend.services import location_service

router = APIRouter()


@router.get("/locations", response_model=list[LocationRead], status_code=200)
async def list_locations(
    client: AsyncClient = Depends(get_supabase),
) -> list[LocationRead]:
    """List all locations ordered by city.

    Args:
        client: Injected async Supabase client.

    Returns:
        List of all locations.
    """
    return await location_service.get_all_locations(client)
