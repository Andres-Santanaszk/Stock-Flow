from db.connection import get_connection

class Movement:
    def __init__(
        self, 
        id_item, 
        id_user, 
        mov_type, 
        reason, 
        qty, 
        from_location_id=None, 
        to_location_id=None,
        id_mov=None,
        created_at=None
    ):
        self.id_mov = id_mov
        self.id_item = id_item
        self.id_user = id_user
        self.mov_type = mov_type
        self.reason = reason
        self.qty = qty
        self.from_location_id = from_location_id
        self.to_location_id = to_location_id
        self.created_at = created_at
    
    def save(self):
        sql = """
        INSERT INTO movements
            (id_item, id_user, type, reason, qty, from_location_id, to_location_id)
        VALUES
            (%s,%s,%s,%s,%s,%s,%s)
        RETURNING id_mov, created_at;
        """
        
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (
                self.id_item,
                self.id_user,
                self.mov_type,
                self.reason,
                self.qty,
                self.from_location_id,
                self.to_location_id
            ))

            row = cur.fetchone()
            conn.commit()

            self.id_mov = row[0]
            self.created_at = row[1]

            return self.id_mov
            
        except Exception as e:
            conn.rollback()
            raise e 
        finally:
            cur.close()
            conn.close()
    
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