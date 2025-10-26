from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Enum as SAEnum
from ..base import Base
from .enums import UomType

class Uom(Base):
    __tablename__ = "uom"

    id_uom: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)     # Kilogramo, Litro, Unidad
    symbol: Mapped[str] = mapped_column(String, unique=True, nullable=False)   # kg, L, un
    type: Mapped[UomType] = mapped_column(SAEnum(UomType, name="uom_type"), nullable=False)

    item_uoms = relationship("ItemUom", back_populates="uom", cascade="all, delete-orphan")
