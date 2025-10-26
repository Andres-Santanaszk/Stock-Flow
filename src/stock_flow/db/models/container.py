from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Boolean, Text, Enum as SAEnum, String
from ..base import Base
from .enums import ContainerType

class Container(Base):
    __tablename__ = "containers"

    id_container: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[ContainerType] = mapped_column(SAEnum(ContainerType, name="container_type"), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")

    item_containers = relationship("ItemContainer", back_populates="container", cascade="all, delete-orphan")
