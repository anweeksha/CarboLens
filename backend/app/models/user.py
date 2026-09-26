"""User model."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.activity import Activity
    from app.models.department import Department
    from app.models.hostel import Hostel


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    department_id: Mapped[int | None] = mapped_column(
        ForeignKey("departments.id"),
        nullable=True,
        index=True,
    )
    hostel_id: Mapped[int | None] = mapped_column(
        ForeignKey("hostels.id"),
        nullable=True,
        index=True,
    )
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    user_type: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    department: Mapped[Department | None] = relationship(back_populates="users")
    hostel: Mapped[Hostel | None] = relationship(back_populates="users")
    activities: Mapped[list[Activity]] = relationship(back_populates="user")
