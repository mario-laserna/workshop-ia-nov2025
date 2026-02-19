"""Generic pagination schema for paginated API responses."""

from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper.

    Attributes:
        items: List of items for the current page.
        total: Total number of items across all pages.
        page: Current page number (1-based).
        size: Number of items per page.
        total_pages: Total number of pages.
    """

    items: list[T]
    total: int
    page: int
    size: int
    total_pages: int
