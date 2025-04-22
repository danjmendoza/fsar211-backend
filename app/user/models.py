from datetime import datetime
from db import Base
from sqlalchemy import func, Column, Integer, String, TIMESTAMP, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    # last_name: Mapped[Optional[str]] = None
    resource_type: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[datetime | None]

    def __repr__(self) -> str:
        return f"User(id={self.id})"