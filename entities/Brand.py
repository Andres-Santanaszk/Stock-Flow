from db.connection import get_connection


class Brand:
    def __init__(self, id_brand=None, name=None, description=None, website=None, contact_email=None, created_at=None):
        self.id_brand = id_brand
        self.name = name
        self.description = description
        self.website = website
        self.contact_email = contact_email
        self.created_at = created_at

    def add_brand(self):
        if self.id_brand is not None:
            return self.update()

        if self.name is None:
            raise ValueError(
                "El atributo 'name' no puede ser nulo para agregar una nueva marca.")

        sql = """
        INSERT INTO brands (name, description, website, contact_email)
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
                self.contact_email
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
                self.id_brand
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
<<<<<<< HEAD
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM brands") # Trae todo
        rows = cursor.fetchall()
        conn.close()
        
        # Convertimos los resultados en una lista de objetos Brand
        brands_list = []
        for row in rows:
            # Asumiendo que el orden en DB es id, name, desc, web, email, date
            new_brand = Brand(id_brand=row[0], name=row[1], description=row[2], website=row[3], contact_email=row[4])
            brands_list.append(new_brand)
        return brands_list
=======
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
>>>>>>> localizacion

    def __repr__(self):
        return f"<Brand name={self.name} id={self.id_brand}>"
