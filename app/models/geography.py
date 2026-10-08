from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Geography(Base):
    __tablename__ = "geographies"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    level: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    parent_id: Mapped[str | None] = mapped_column(
        ForeignKey("geographies.id"),
        nullable=True,
    )

    code: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        unique=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    parent: Mapped["Geography | None"] = relationship(
        "Geography",
        remote_side=[id],
        back_populates="children",
    )

    children: Mapped[list["Geography"]] = relationship(
        "Geography",
        back_populates="parent",
    )