from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey
from ..base import Base

class User(Base):
    __tablename__ = "users"

    id_user: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    role_id: Mapped[int | None] = mapped_column(ForeignKey("roles.id"))

    role = relationship("Role", back_populates="users")
    movements = relationship("Movement", back_populates="user")
