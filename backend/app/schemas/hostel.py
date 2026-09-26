"""Hostel schemas."""

from pydantic import BaseModel, ConfigDict, Field


class HostelRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str = Field(min_length=1, max_length=255)
