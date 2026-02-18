"""Supabase async client configuration and dependency injection."""

from typing import AsyncGenerator

from supabase._async.client import AsyncClient, create_client

from backend.core.settings import settings


async def _create_supabase_client() -> AsyncClient:
    """Create and return an async Supabase client instance.

    Returns:
        AsyncClient: Configured Supabase async client.
    """
    return await create_client(
        supabase_url=settings.supabase_url,
        supabase_key=settings.supabase_key,
    )


async def get_supabase() -> AsyncGenerator[AsyncClient, None]:
    """FastAPI dependency that provides an async Supabase client.

    Yields:
        AsyncClient: Supabase async client for use in request handlers.
    """
    client = await _create_supabase_client()
    yield client
