from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text
from ..base import Base

class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)  # e.g., item_view, movement_register
    description: Mapped[str | None] = mapped_column(Text)

    role_permissions = relationship("RolePermission", back_populates="permission", cascade="all, delete-orphan")
