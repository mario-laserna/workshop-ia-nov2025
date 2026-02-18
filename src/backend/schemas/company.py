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
        total_funding: Total funding received (in USD).
        arr: Annual Recurring Revenue (in USD).
        valuation: Company valuation (in USD).
    """

    id: int
    name: str
    industry: str
    location: str
    products: str
    founding_year: int
    total_funding: int
    arr: int
    valuation: int


CompanyListResponse = PaginatedResponse[CompanyRead]
"""Type alias for a paginated response of companies."""
