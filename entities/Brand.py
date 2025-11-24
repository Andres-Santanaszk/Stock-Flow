from db.connection import get_connection


class Brand:
    def __init__(self, id_brand=None, name=None, description=None, website=None,active=True, contact_email=None, created_at=None):
        self.id_brand = id_brand
        self.name = name
        self.description = description
        self.website = website
        self.active=active
        self.contact_email = contact_email
        self.created_at = created_at

    def add_brand(self):
        if self.id_brand is not None:
            return self.update()

        if self.name is None:
            raise ValueError(
                "El atributo 'name' no puede ser nulo para agregar una nueva marca.")

        sql = """
        INSERT INTO brands (name, description, website, contact_email, active)
        VALUES (%s, %s, %s, %s)
        RETURNING id_brand, created_at;
        """

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (
                self.name,
                self.description,
                self.website,
                self.contact_email,
                self.active
            ))
            row = cur.fetchone()
            conn.commit()

            self.id_brand = row[0]
            self.created_at = row[1]
            return self.id_brand

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    def update(self):
        if self.id_brand is None:
            raise ValueError("No se puede actualizar una marca sin id_brand.")

        if self.name is None:
            raise ValueError(
                "El atributo 'name' no puede ser nulo para actualizar.")

        sql = """
        UPDATE brands
           SET name = %s,
               description = %s,
               website = %s,
               contact_email = %s
               active = %s
         WHERE id_brand = %s;
        """

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (
                self.name,
                self.description,
                self.website,
                self.contact_email,
                self.id_brand,
                self.active
            ))
            conn.commit()
            return self.id_brand

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_all_brands():
        """
        Recupera el ID y el nombre de todas las marcas (ideales para QComboBox).
        Devuelve una lista de tuplas: [(id_brand, name), ...].
        """
        sql = """
        SELECT id_brand, name
        FROM brands
        ORDER BY name;
        """

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            return rows

        except Exception as e:
            raise e
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_by_id(id_brand):
        sql = """
        SELECT
            id_brand, name, description, website, contact_email, active, created_at
        FROM brands
        WHERE id_brand = %s;
        """

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (id_brand,))
            row = cur.fetchone()
            if not row:
                return None

            return Brand(
                id_brand=row[0],
                name=row[1],
                description=row[2],
                website=row[3],
                contact_email=row[4],
                created_at=row[5],
            )
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def has_associated_items(id_brand):
        """
        Busca en la tabla 'items' si existe alguno con este brand_id.
        """
        sql = "SELECT 1 FROM items WHERE brand_id = %s LIMIT 1"
        
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (id_brand,))
            row = cur.fetchone()
            # Retorna True si encontró al menos un item
            return True if row else False
        except Exception as e:
            print(f"Error checking brand items: {e}")
            return False
        finally:
            cur.close()
            conn.close()
    
    def __repr__(self):
        return f"<Brand name={self.name} id={self.id_brand}>"
