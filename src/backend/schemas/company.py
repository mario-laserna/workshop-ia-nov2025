"""Pydantic schemas for Company."""

from pydantic import BaseModel

from backend.schemas.pagination import PaginatedResponse


class CompanyRead(BaseModel):
    """Schema for reading a company record.

    Attributes:
        id: Unique identifier of the company.
        name: Company name.
        industry: Industry name as a string.
        location: Formatted location string ("City, Country").
        products: Main products or services.
        founding_year: Year the company was founded.
        total_funding: Total funding received (in USD), nullable.
        arr: Annual Recurring Revenue (in USD), nullable.
        valuation: Company valuation (in USD), nullable.
    """

    id: int
    name: str
    industry: str
    location: str
    products: str
    founding_year: int | None = None
    total_funding: int | None = None
    arr: int | None = None
    valuation: int | None = None


CompanyListResponse = PaginatedResponse[CompanyRead]
"""Type alias for a paginated response of companies."""
