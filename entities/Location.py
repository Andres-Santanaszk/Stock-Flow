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
    def get_all():
        sql = """
        SELECT 
            id_location, code, type, description, active 
        FROM locations 
        WHERE active = TRUE 
        ORDER BY code;
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            locations = []
            for row in rows:
                # row[0] = id_location
                # row[1] = code
                # row[2] = type
                # row[3] = description
                # row[4] = active
                
                # CORRECCIÓN: Inicializar la clase con los atributos correctos
                locations.append(Location(
                    id_location=row[0], 
                    code=row[1], 
                    type=row[2],
                    description=row[3],
                    active=row[4]
                ))
            return locations
            
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()