"""User schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    department_id: int | None = None
    hostel_id: int | None = None
    year: int | None = Field(default=None)
    user_type: str
    created_at: datetime
