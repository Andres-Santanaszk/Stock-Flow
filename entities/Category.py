from db.connection import get_connection


class Category:
    def __init__(
        self,
        id_category=None,
        name=None,
        class_=None,
        description=None,
        active=True,
        created_at=None,
        updated_at=None
    ):
        self.id_category = id_category
        self.name = name
        self.class_ = class_
        self.description = description
        self.active = active
        self.created_at = created_at
        self.updated_at = updated_at

    def add_category(self):
        """
        Inserta una nueva categoría en la base de datos.
        Si el objeto ya tiene un id_category, llama a update() en su lugar.
        """
        if self.id_category is not None:
            return self.update()

        if self.name is None or self.class_ is None:
            raise ValueError(
                "Los atributos 'name' y 'class_' no pueden ser nulos.")

        sql = """
        INSERT INTO categories (name, class, description, active)
        VALUES (%s, %s, %s, %s)
        RETURNING id_category, created_at, updated_at;
        """

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (
                self.name,
                self.class_,
                self.description,
                self.active
            ))
            row = cur.fetchone()
            conn.commit()

            self.id_category = row[0]
            self.created_at = row[1]
            self.updated_at = row[2]
            return self.id_category

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    def update(self):
        if self.id_category is None:
            raise ValueError(
                "No se puede actualizar una categoría sin id_category.")

        if self.name is None or self.class_ is None:
            raise ValueError(
                "Los atributos 'name' y 'class_' no pueden ser nulos.")

        sql = """
        UPDATE categories
           SET name = %s,
               class = %s,
               description = %s,
               active = %s
         WHERE id_category = %s
         RETURNING updated_at;
        """

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (
                self.name,
                self.class_,
                self.description,
                self.active,
                self.id_category
            ))
            row = cur.fetchone()
            conn.commit()

            self.updated_at = row[0]
            return self.id_category

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_all_categories():
        """
        Recupera el ID y el nombre de todas las categorías (ideales para QComboBox).
        Devuelve una lista de tuplas: [(id_category, name), ...].
        """
        sql = """
        SELECT id_category, name
        FROM categories
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

    def __repr__(self):
        return f"<Category name={self.name} id={self.id_category}>"
