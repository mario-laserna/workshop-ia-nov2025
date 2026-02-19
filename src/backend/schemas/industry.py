"""Pydantic schemas for Industry."""

from pydantic import BaseModel


class IndustryRead(BaseModel):
    """Schema for reading an industry record.

    Attributes:
        id: Unique identifier of the industry.
        name: Name of the industry.
    """

    id: int
    name: str
