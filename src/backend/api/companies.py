"""Router for company endpoints."""

from fastapi import APIRouter, Depends, Query
from supabase._async.client import AsyncClient

from backend.core.supabase_client import get_supabase
from backend.schemas.company import CompanyListResponse
from backend.services import company_service

router = APIRouter()


@router.get("/companies", response_model=CompanyListResponse, status_code=200)
async def list_companies(
    industry_id: int | None = Query(default=None, description="Filter by industry ID"),
    location_id: int | None = Query(default=None, description="Filter by location ID"),
    page: int = Query(default=1, ge=1, description="Page number (1-based)"),
    size: int = Query(default=20, ge=1, le=100, description="Items per page"),
    client: AsyncClient = Depends(get_supabase),
) -> CompanyListResponse:
    """List companies with optional filters and pagination.

    Args:
        industry_id: Optional filter by industry ID.
        location_id: Optional filter by location ID.
        page: Page number, starting from 1.
        size: Number of items per page (1-100).
        client: Injected async Supabase client.

    Returns:
        Paginated list of companies with metadata.
    """
    return await company_service.get_companies(
        client,
        industry_id=industry_id,
        location_id=location_id,
        page=page,
        size=size,
    )
