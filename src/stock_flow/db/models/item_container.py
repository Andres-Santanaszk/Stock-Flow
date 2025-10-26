from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Numeric, ForeignKey, UniqueConstraint, Index
from ..base import Base

class ItemContainer(Base):
    __tablename__ = "item_containers"

    # PK surrogate (más simple para ORM y futuras FKs)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # FKs
    id_item: Mapped[int] = mapped_column(ForeignKey("items.id_item"), nullable=False)
    id_container: Mapped[int] = mapped_column(ForeignKey("containers.id_container"), nullable=False)

    # Slot físico dentro del contenedor (ej: "A1", "Bin-003", "Pal-491")
    location: Mapped[str] = mapped_column(String, nullable=False)

    # Cantidad almacenada en ese slot
    qty: Mapped[float] = mapped_column(Numeric(18, 3), nullable=False, default=0, server_default="0")

    __table_args__ = (
        
        UniqueConstraint("id_container", "location", name="uq_item_containers_container_location"),
        # Índice de apoyo para buscar rápido por item+container
        Index("ix_item_containers_item_container", "id_item", "id_container"),
    )

    # Relaciones ORM
    item = relationship("Item", back_populates="item_containers")
    container = relationship("Container", back_populates="item_containers")
