from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Integer, Numeric, DateTime, func, String, Enum as SAEnum, ForeignKey, Index
from ..base import Base
from .enums import MovType, MovReason

class Movement(Base):
    __tablename__ = "movements"

    id_mov: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    id_item: Mapped[int] = mapped_column(ForeignKey("items.id_item"), nullable=False)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id_user"), nullable=False)
    type: Mapped[MovType] = mapped_column(SAEnum(MovType, name="mov_type"), nullable=False, default=MovType.OUT, server_default=MovType.OUT.value)
    qty: Mapped[float] = mapped_column(Numeric(18, 3), nullable=False)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    reason: Mapped[MovReason] = mapped_column(SAEnum(MovReason, name="mov_reason"), nullable=False)
    source: Mapped[str | None] = mapped_column(String)
    target: Mapped[str | None] = mapped_column(String)

    item = relationship("Item", back_populates="movements")
    user = relationship("User", back_populates="movements")


Index("ix_movements_id_item", Movement.id_item)
Index("ix_movements_created_at", Movement.created_at)
