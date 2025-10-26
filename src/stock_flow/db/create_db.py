from .engine import engine
from .base import Base

from .models import (
    Brand, Container, Item, ItemContainer, Movement,
    Role, Permission, RolePermission, User,
    Uom, ItemUom,
)

def create_all():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_all()
    print("Tablas creadas con éxito.")
