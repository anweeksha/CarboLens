"""Activity log model."""

from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import Date, DateTime, ForeignKey, Index, JSON, Numeric, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = (
        Index("ix_activities_user_id_activity_date", "user_id", "activity_date"),
        Index("ix_activities_category_activity_type", "category", "activity_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    activity_type: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    quantity: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False)
    unit: Mapped[str] = mapped_column(String(32), nullable=False)
    activity_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    # Historical emission preservation columns
    emission: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False)
    emission_factor_used: Mapped[float | None] = mapped_column(Numeric(24, 12), nullable=True)
    emission_factor_source: Mapped[str | None] = mapped_column(String(512), nullable=True)

    activity_metadata: Mapped[dict[str, Any] | None] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped[User] = relationship(back_populates="activities")
