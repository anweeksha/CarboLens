"""ChallengeProgress model."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.challenge import Challenge
    from app.models.user import User


class ChallengeProgress(Base):
    __tablename__ = "challenge_progress"
    __table_args__ = (
        UniqueConstraint("challenge_id", "user_id", name="uq_challenge_user"),
        Index("ix_challenge_progress_challenge_user", "challenge_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    challenge_id: Mapped[int] = mapped_column(ForeignKey("challenges.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    baseline_emission: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False, default=0.0)
    baseline_quantity: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False, default=0.0)
    baseline_status: Mapped[str] = mapped_column(String(64), nullable=False, default="calculated")

    current_emission: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False, default=0.0)
    current_quantity: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False, default=0.0)
    saved_emission: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False, default=0.0)
    completion_percentage: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0.0)

    status: Mapped[str] = mapped_column(String(64), nullable=False, default="in_progress")
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    last_updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    challenge: Mapped[Challenge] = relationship("Challenge", back_populates="progress_records")
    user: Mapped[User] = relationship("User")
