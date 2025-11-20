from db.connection import get_connection  # Asumo que tienes esto configurado


class Location:
    def __init__(
        self,
        code,
        type,
        description="",
        active=True,
        id_location=None
    ):
        self.id_location = id_location
        self.type = type
        self.code = code
        self.description = description
        self.active = active

    def add_location(self):
        if self.id_location is not None:
            return self.id_location

        sql = """
        INSERT INTO locations
            (code, type, description, active)
        VALUES
            (%s,%s,%s,%s)
        RETURNING id_location;
        """

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (
                self.code,
                self.type,
                self.description,
                self.active
            ))
            self.id_location = cur.fetchone()[0]
            conn.commit()

            return self.id_location
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_all_locations_for_combo():
        """
        Retorna una lista de tuplas (id_location, code, type)
        Ideal para llenar QComboBox.
        """
        sql = "SELECT id_location, code, type FROM locations WHERE active = TRUE ORDER BY code;"
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql)
            return cur.fetchall()
        except Exception as e:
            raise e
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_unique_values_for_field(field_name):
        """
        Retorna una lista de valores únicos y ordenados para un campo específico (type o code).
        """
        # **Seguridad:** Mapear el nombre del campo para evitar inyección SQL en el nombre de la columna.
        safe_fields = {'type': 'type', 'code': 'code'}
        db_field = safe_fields.get(field_name)

        if not db_field:
            raise ValueError(f"Campo de filtrado no válido: {field_name}")

        sql = f"SELECT DISTINCT {db_field} FROM locations ORDER BY {db_field};"

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql)
            # Retorna solo el valor único de la tupla (ej: ('Rack',), ('Shelf',) -> ['Rack', 'Shelf'])
            return [row[0] for row in cur.fetchall()]
        except Exception as e:
            raise e
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_all_locations_data(filter_field=None, filter_value=None, search_term=None):
        """
        Retorna una lista de tuplas con todos los campos:
        (id_location, type, code, description, active)
        Aplica filtro y/o término de búsqueda si se proporcionan.
        La lógica de búsqueda usa el operador LIKE en code o description.
        """
        sql = """
        SELECT id_location, type, code, description, active
        FROM locations
        """
        params = []
        where_clauses = []

        # 1. Filtro por campo y valor (type o code)
        if filter_field and filter_value:
            safe_fields = {'type': 'type', 'code': 'code'}
            db_field = safe_fields.get(filter_field)

            if db_field:
                where_clauses.append(f"{db_field} = %s")
                params.append(filter_value)

        # 2. Filtro por término de búsqueda (LIKE) en code o description
        if search_term:
            # Usamos ILIKE para búsqueda insensible a mayúsculas/minúsculas en PostgreSQL
            # Buscamos coincidencias parciales en code o description
            search_clause = "(code ILIKE %s OR description ILIKE %s)"
            where_clauses.append(search_clause)

            # El término de búsqueda debe estar rodeado de '%' para LIKE/ILIKE
            like_term = f"%{search_term}%"
            # Agregamos el término 2 veces para los 2 %s
            params.extend([like_term, like_term])

        # 3. Construir la cláusula WHERE final
        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)

        sql += " ORDER BY id_location;"

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, params)
            return cur.fetchall()
        except Exception as e:
            raise e
        finally:
            cur.close()
            conn.close()
