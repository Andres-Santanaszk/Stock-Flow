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

    def update(self):
        if self.id_location is None:
            raise ValueError("No se puede actualizar una marca sin id_location.")

        if self.code is None:
            raise ValueError(
                "El atributo 'code' no puede ser nulo para actualizar.")

        sql = """
        UPDATE locations
           SET type = %s,
               code = %s,
               description = %s,
               active = %s
         WHERE id_location = %s;
        """

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (
                self.type,
                self.code,
                self.description,
                self.active,
                self.id_location
            ))
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
        sql = "SELECT id_location, code, type FROM locations ORDER BY code;"
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
        safe_fields = {'type': 'type', 'code': 'code'}
        db_field = safe_fields.get(field_name)

        if not db_field:
            raise ValueError(f"Campo de filtrado no válido: {field_name}")

        sql = f"SELECT DISTINCT {db_field} FROM locations ORDER BY {db_field};"

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

        if filter_field and filter_value:
            safe_fields = {'type': 'type', 'code': 'code'}
            db_field = safe_fields.get(filter_field)

            if db_field:
                where_clauses.append(f"{db_field} = %s")
                params.append(filter_value)

        if search_term:
            search_clause = "(code ILIKE %s OR description ILIKE %s)"
            where_clauses.append(search_clause)

            like_term = f"%{search_term}%"
            params.extend([like_term, like_term])
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

    @staticmethod
    def get_by_id(id_location):
        sql = """
        SELECT
            id_location, type, code, description, active
        FROM locations
        WHERE id_location = %s;
        """

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (id_location,))
            row = cur.fetchone()
            if not row:
                return None

            return Location(
                id_location=row[0],
                type=row[1],
                code=row[2],
                description=row[3],
                active=row[4],
            )
        finally:
            cur.close()
            conn.close()
            
    def __repr__(self):
        return f"<Location code={self.code} id={self.id_location}>"