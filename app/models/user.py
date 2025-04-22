from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    resource_type = Column(String, nullable=True)
    published = Column(Boolean, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))