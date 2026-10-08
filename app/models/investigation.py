from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Investigation(Base):
    __tablename__ = "investigations"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    query: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    disease: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    geography: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
    )

    data_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="synthetic_demo",
    )

    risk_level: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    human_review_required: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )