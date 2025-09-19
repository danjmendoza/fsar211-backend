from datetime import datetime

from db import Base
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Form211(Base):
    __tablename__ = "form211"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(nullable=False)
    operational_period: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    closed_at: Mapped[datetime | None] = mapped_column(nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)
    creator: Mapped["User"] = relationship(back_populates="forms211")  # noqa

    def __repr__(self) -> str:
        return f"Form211(id={self.id})"
