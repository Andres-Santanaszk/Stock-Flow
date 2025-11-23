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

    @staticmethod
    def get_last_movements_by_item(id_item, limit=2):
        """
        Obtiene los últimos N movimientos de un ítem específico,
        incluyendo códigos de ubicación origen/destino.
        """
        sql = """
        SELECT 
            m.type,
            m.reason,
            m.qty,
            m.created_at,
            COALESCE(lf.code, '-') as from_code,
            COALESCE(lt.code, '-') as to_code,
            u.full_name
        FROM movements m
        LEFT JOIN locations lf ON m.from_location_id = lf.id_location
        LEFT JOIN locations lt ON m.to_location_id = lt.id_location
        LEFT JOIN users u ON m.id_user = u.id_user
        WHERE m.id_item = %s
        ORDER BY m.created_at DESC
        LIMIT %s;
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (id_item, limit))
            return cur.fetchall()
        except Exception as e:
            print(f"Error fetching last movements: {e}")
            return []
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_history_data(filter_type=None, date_from=None, date_to=None):
        """
        Obtiene el historial filtrado por Tipo y Rango de Fechas.
        Construye la consulta SQL dinámicamente.
        """
        sql = """
        SELECT 
            m.id_mov,
            m.created_at,
            i.name AS item_name,
            i.sku,
            m.type,
            m.reason,
            m.qty,
            u.full_name AS user_name,
            COALESCE(lf.code, '-') AS origin,
            COALESCE(lt.code, '-') AS dest
        FROM movements m
        JOIN items i ON m.id_item = i.id_item
        JOIN users u ON m.id_user = u.id_user
        LEFT JOIN locations lf ON m.from_location_id = lf.id_location
        LEFT JOIN locations lt ON m.to_location_id = lt.id_location
        """

        params = []
        where_clauses = []

        if filter_type and filter_type != "Todos":
            where_clauses.append("m.type = %s")
            params.append(filter_type)

        if date_from:
            where_clauses.append("m.created_at >= %s")
            params.append(f"{date_from} 00:00:00")

        if date_to:
            where_clauses.append("m.created_at <= %s")
            params.append(f"{date_to} 23:59:59")

        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)

        sql += " ORDER BY m.created_at DESC;"

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, tuple(params))
            return cur.fetchall()
        except Exception as e:
            print(f"Error en get_history_data: {e}")
            return []
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_unique_values_for_field(field_name):
        """
        Retorna una lista de valores únicos y ordenados para un campo específico (type o reason).
        """
        safe_fields = {'type': 'type', 'reason': 'reason'}
        db_field = safe_fields.get(field_name)

        if not db_field:
            raise ValueError(f"Campo de filtrado no válido: {field_name}")

        sql = f"SELECT DISTINCT {db_field} FROM movements ORDER BY {db_field};"

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql)
            return [row[0] for row in cur.fetchall()]
        except Exception as e:
            raise e
        finally:
            cur.close()
            conn.close()

    def __repr__(self):
        """
        Devuelve una representación corta del movimiento con su tipo, cantidad y artículo
        """
        pass
