from db.connection import get_connection
from ui.translations import ITEM_LABELS_ES, ITEM_PACK_TYPE_ES, BOOL_ES


class Item:
    def __init__(
        self,
        name,
        sku,
        description="",
        pack_type="unit",
        min_qty=0,
        active=True,
        barcode=None,
        brand_id=None,
        category_id=None,
        id_item=None,
        created_at=None,
        updated_at=None,
    ):
        self.id_item = id_item
        self.name = name
        self.sku = sku
        self.barcode = barcode
        self.brand_id = brand_id
        self.description = description
        self.category_id = category_id
        self.pack_type = pack_type
        self.min_qty = min_qty
        self.active = active
        self.created_at = created_at
        self.updated_at = updated_at

    def add_item(self):
        if self.id_item is not None:
            return self.update()

        sql = """
        INSERT INTO items
            (name, sku, barcode, brand_id, description, category_id, pack_type, min_qty, active)
        VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id_item, created_at, updated_at;
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (
                self.name,
                self.sku,
                self.barcode,
                self.brand_id,
                self.description,
                self.category_id,
                self.pack_type,
                self.min_qty,
                self.active
            ))
            row = cur.fetchone()
            conn.commit()

            self.id_item = row[0]
            self.created_at = row[1]
            self.updated_at = row[2]
            return self.id_item
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    def update(self):
        if self.id_item is None:
            raise ValueError(
                "No puedes actualizar un item sin id_item. agregalo primero.")

        sql = """
        UPDATE items
           SET name        = %s,
               sku         = %s,
               barcode     = %s,
               brand_id    = %s,
               description = %s,
               category_id = %s,
               pack_type   = %s,
               min_qty     = %s,
               active      = %s
         WHERE id_item = %s
        RETURNING updated_at;
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (
                self.name,
                self.sku,
                self.barcode,
                self.brand_id,
                self.description,
                self.category_id,
                self.pack_type,
                self.min_qty,
                self.active,
                self.id_item
            ))
            row = cur.fetchone()
            if not row:
                raise ValueError(f"No existe items.id_item = {self.id_item}")

            conn.commit()
            self.updated_at = row[0]
            return self.updated_at
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_by_id(id_item):
        sql = """
        SELECT
            id_item, name, sku, barcode, brand_id, description, category_id,
            pack_type, min_qty, active, created_at, updated_at
        FROM items
        WHERE id_item = %s;
        """

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (id_item,))
            row = cur.fetchone()
            if not row:
                return None

            return Item(
                id_item=row[0],
                name=row[1],
                sku=row[2],
                barcode=row[3],
                brand_id=row[4],
                description=row[5],
                category_id=row[6],
                pack_type=row[7],
                min_qty=row[8],
                active=row[9],
                created_at=row[10],
                updated_at=row[11],
            )
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def exists_sku(sku):
        sql = "SELECT 1 FROM items WHERE sku = %s LIMIT 1;"
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (sku,))
            return cur.fetchone() is not None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    # Limit son los resultados que queremos, offset los que queremos ignorar
    def search_by_name(name_fragment, limit=100, offset=0):
        sql = """
        SELECT
            id_item, name, sku, barcode, brand_id, description, category_id,
            pack_type, min_qty, active, created_at, updated_at
        FROM items
        WHERE (%s = '' OR LOWER(name) LIKE LOWER(%s))
        ORDER BY name
        LIMIT %s OFFSET %s;
        """
        pattern = f"%{name_fragment}%" if name_fragment else ""
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (name_fragment or "", pattern, limit, offset))
            rows = cur.fetchall()

            results = []
            for row in rows:
                results.append(Item(
                    id_item=row[0],
                    name=row[1],
                    sku=row[2],
                    barcode=row[3],
                    brand_id=row[4],
                    description=row[5],
                    category_id=row[6],
                    pack_type=row[7],
                    min_qty=row[8],
                    active=row[9],
                    created_at=row[10],
                    updated_at=row[11],
                ))
            return results
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def search_by_category(category_id, limit=100, offset=0):
        """
        Busca todos los ítems que pertenecen a una categoría específica,
        con paginación.
        """
        sql = """
        SELECT
            id_item, name, sku, barcode, brand_id, description, category_id,
            pack_type, min_qty, active, created_at, updated_at
        FROM items
        WHERE category_id = %s  -- <-- La condición de búsqueda
        ORDER BY name
        LIMIT %s OFFSET %s;
        """

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (category_id, limit, offset))
            rows = cur.fetchall()

            results = []
            for row in rows:
                results.append(Item(
                    id_item=row[0],
                    name=row[1],
                    sku=row[2],
                    barcode=row[3],
                    brand_id=row[4],
                    description=row[5],
                    category_id=row[6],
                    pack_type=row[7],
                    min_qty=row[8],
                    active=row[9],
                    created_at=row[10],
                    updated_at=row[11],
                ))
            return results
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_all_brands_for_combo():
        sql = "SELECT id_brand, name FROM brands ORDER BY name;"
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
    def get_all_categories_for_combo():
        sql = "SELECT id_category, name FROM categories WHERE active = TRUE ORDER BY name;"
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
    def search_items_for_display(name_fragment, limit=100, offset=0):
        """
        Busca ítems para MOSTRAR en una tabla (con JOINs) y
        soporta paginación (LIMIT/OFFSET).
        """
        sql = """
        SELECT
            i.id_item, 
            i.name AS item_name, 
            i.sku,
            i.active,
            b.name AS brand_name,   
            c.name AS category_name 
        FROM items i
        LEFT JOIN brands b ON i.brand_id = b.id_brand
        LEFT JOIN categories c ON i.category_id = c.id_category
        WHERE (%s = '' OR LOWER(i.name) LIKE LOWER(%s))
        ORDER BY i.name
        LIMIT %s OFFSET %s; 
        """

        pattern = f"%{name_fragment}%" if name_fragment else ""
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (name_fragment or "", pattern, limit, offset))

            return cur.fetchall()
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_all_items_data():
        """
        Recupera todos los campos de todos los ítems.
        Devuelve una lista de tuplas con los datos completos del ítem,
        ideal para que load_items_data() pueda filtrarlos y mostrarlos.
        """
        sql = """
        SELECT
            id_item, 
            name, 
            sku, 
            barcode, 
            brand_id, 
            description, 
            category_id, 
            pack_type, 
            min_qty, 
            active, 
            created_at, 
            updated_at
        FROM items
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
        return f"<Item name={self.name} sku={self.sku} id={self.id_item}>"
