# src/stock_flow/db/base.py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Clase base del ORM. Todos los modelos deben heredar de aquí."""
    pass
