from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Numeric, ForeignKey, PrimaryKeyConstraint, Index
from ..base import Base

class ItemUom(Base):
    __tablename__ = "item_uom"

    id_item: Mapped[int] = mapped_column(ForeignKey("items.id_item"), nullable=False)
    id_uom: Mapped[int] = mapped_column(ForeignKey("uom.id_uom"), nullable=False)
    uom_value: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False)  # p.ej. 236 g por unidad

    __table_args__ = (
        PrimaryKeyConstraint("id_item", "id_uom", name="pk_item_uom"),
        Index("ix_item_uom_id_uom", "id_uom"),
    )

    item = relationship("Item", back_populates="item_uoms")
    uom = relationship("Uom", back_populates="item_uoms")
