from datetime import datetime

from db import Base
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column


class Timelog(Base):
    __tablename__ = "timelog"
    __table_args__ = {"extend_existing": True}

    """
    id, auto increment id just for db.
    form211_id, foreign key to form211 table
    created_by, who created this entry. 
    sar_id, search and rescue id, for non members it can be null
    name
    resource_type
    arrival datetime
    initials_out
    departure datetime
    """

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    form211_id: Mapped[int] = mapped_column(ForeignKey("form211.id"))
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    sar_id: Mapped[int] = mapped_column(default=0, nullable=True)
    name: Mapped[str] = mapped_column(nullable=False)
    resource_type: Mapped[str] = mapped_column(nullable=False)
    arrival_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    departure_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"Timelog(id={self.id})"
