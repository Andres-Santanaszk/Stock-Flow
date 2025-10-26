from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, Numeric, DateTime, func, ForeignKey, Enum as SAEnum, Index
from ..base import Base
from .enums import ItemType

class Item(Base):
    __tablename__ = "items"

    id_item: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    sku: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    barcode: Mapped[str | None] = mapped_column(String(14), unique=True)
    type: Mapped[ItemType] = mapped_column(SAEnum(ItemType, name="item_type"), nullable=False, default=ItemType.finished_product, server_default=ItemType.finished_product.value)
    item_qty: Mapped[float] = mapped_column(Numeric(18, 3), nullable=False, default=0, server_default="0")
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    brand_id: Mapped[int | None] = mapped_column(ForeignKey("brands.id_brand"))
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    brand = relationship("Brand", back_populates="items")
    movements = relationship("Movement", back_populates="item")
    item_containers = relationship("ItemContainer", back_populates="item", cascade="all, delete-orphan")
    item_uoms = relationship("ItemUom", back_populates="item", cascade="all, delete-orphan")


Index("ix_items_name", Item.name)
