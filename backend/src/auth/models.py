import uuid
from datetime import datetime
from typing import Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import (DATE, JSON, TIMESTAMP, UUID, Boolean, Column,
                        ForeignKey, Integer, String)
from sqlalchemy.orm import relationship

from ..db import Base

UUID_ID = uuid.UUID


class Role(Base):
    __tablename__ = "roles"

    id: int = Column("id", Integer, primary_key=True)
    name: str = Column("name", String, nullable=False)
    permissions: dict = Column("permissions", JSON)

    users = relationship("User", back_populates="role")


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    id: UUID_ID = Column("id", UUID, primary_key=True, default=uuid.uuid4)
    registered_at = Column(
        "registered_at", TIMESTAMP, default=datetime.utcnow
    )
    role_id: int = Column("role_id", Integer, ForeignKey("roles.id"))
    email: str = Column(
        String(length=320), unique=True, index=True, nullable=False
    )
    first_name: str = Column("first_name", String, nullable=True)
    last_name: str = Column("last_name", String, nullable=True)
    birthdate: Optional[datetime.date] = Column("birthdate", DATE)
    password: str = Column(String(length=1024))
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)

    role = relationship("Role", back_populates="users")
    my_posts = relationship("Post", back_populates="author")
    posts = relationship("Post", secondary="likes", back_populates="users")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
