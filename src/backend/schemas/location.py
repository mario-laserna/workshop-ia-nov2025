"""Pydantic schemas for Location."""

from pydantic import BaseModel


class LocationRead(BaseModel):
    """Schema for reading a location record.

    Attributes:
        id: Unique identifier of the location.
        city: City name.
        state: State or province (optional).
        country: Country name.
    """

    id: int
    city: str
    state: str | None
    country: str
