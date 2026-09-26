"""Emission factor model.

Factors are stored in the database. Application code looks them up.
All factors include published source references and source publication years.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Index, Integer, Numeric, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class EmissionFactor(Base):
    __tablename__ = "emission_factors"
    __table_args__ = (
        UniqueConstraint(
            "category",
            "activity_type",
            "unit",
            "region",
            "source_year",
            name="uq_emission_factor_lookup",
        ),
        Index("ix_emission_factors_category_activity_type", "category", "activity_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    activity_type: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    unit: Mapped[str] = mapped_column(String(32), nullable=False)
    factor: Mapped[float] = mapped_column(Numeric(24, 12), nullable=False)
    source: Mapped[str] = mapped_column(String(512), nullable=False)
    source_year: Mapped[int] = mapped_column(Integer, nullable=False)
    region: Mapped[str] = mapped_column(String(64), nullable=False, default="global", index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
