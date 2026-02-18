"""Router for industry endpoints."""

from fastapi import APIRouter, Depends
from supabase._async.client import AsyncClient

from backend.core.settings import settings
from backend.core.supabase_client import get_supabase
from backend.schemas.industry import IndustryRead
from backend.services import industry_service

router = APIRouter()


@router.get("/industries", response_model=list[IndustryRead], status_code=200)
async def list_industries(
    client: AsyncClient = Depends(get_supabase),
) -> list[IndustryRead]:
    """List all industries ordered by name.

    Args:
        client: Injected async Supabase client.

    Returns:
        List of all industries.
    """
    return await industry_service.get_all_industries(client)
