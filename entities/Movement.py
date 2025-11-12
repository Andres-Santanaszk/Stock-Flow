class Movement:
    def __init__(self, 
                id_movement=None, 
                id_item=None, 
                id_user=None, 
                type=None,
                reason=None, 
                qty=None, 
                from_location_id=None, 
                to_location_id=None, 
                created_at=None
                ):
        self.id_movement = id_movement
        self.id_item = id_item
        self.id_user = id_user
        self.type = type
        self.reason = reason
        self.qty = qty
        self.from_location_id = from_location_id
        self.to_location_id = to_location_id
        self.created_at = created_at
    
    def in_(self):
        """
        Registra un movimiento de tipo entrada (IN), como compras, devoluciones o producción terminada
        """
        pass

    def out(self):
        """
        Registra un movimiento de tipo salida (OUT), como ventas, envíos o consumo de materiales
        """
        pass

    def adjust(self):
        """
        Registra un movimiento de ajuste (ADJUST), ya sea por correcciones, daños o ajustes de inventario físico.
        """
        pass

    def last_movements(self):
        """
        Obtiene los últimos movimientos registrados en el sistema.
        """
        pass

    def __repr__(self):
        """
        Devuelve una representación corta del movimiento con su tipo, cantidad y artículo
        """
        pass