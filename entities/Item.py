# entities/item.py
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
            (%s,   %s,  %s,      %s,       %s,          %s,          %s,        %s,      %s)
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
            raise ValueError("No puedes actualizar un item sin id_item. agregalo primero.")

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
            self.updated_at = row[0]   # Valor que puso el trigger
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
        
    def to_display_dict(self, fields=None):
        data = {
            "id_item": self.id_item,
            "name": self.name,
            "sku": self.sku,
            "barcode": self.barcode or "",
            "brand_id": self.brand_id or "",
            "description": self.description or "",
            "category_id": self.category_id or "",
            "pack_type": ITEM_PACK_TYPE_ES.get(self.pack_type, self.pack_type),
            "min_qty": self.min_qty,
            "active": BOOL_ES.get(self.active, str(self.active)),
            "created_at": self.created_at.strftime("%d/%m/%Y %H:%M") if self.created_at else "",
            "updated_at": self.updated_at.strftime("%d/%m/%Y %H:%M") if self.updated_at else "",
        }

        if fields is None:
            fields = data.keys()
            
        return {ITEM_LABELS_ES[k]: data[k] for k in fields if k in data}
   
        
    def __repr__(self):
        return f"<Item name={self.name!r} sku={self.sku!r} id={self.id_item}>"
