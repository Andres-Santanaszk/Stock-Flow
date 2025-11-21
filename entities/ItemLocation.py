from db.connection import get_connection


class ItemLocation:
    def __init__(self, id_item=None, id_location=None, qty=0):
        self.id_item = id_item
        self.id_location = id_location
        self.qty = qty

    @staticmethod
    def get_qty(id_item, id_location):
        sql = "SELECT qty FROM item_locations WHERE id_item = %s AND id_location = %s"
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (id_item, id_location))
            row = cur.fetchone()
            return row[0] if row else 0
        except Exception as e:
            print(f"Error getting qty: {e}")
            return 0
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def list_by_item(id_item):
        sql = """
        SELECT 
            il.id_location, 
            l.code, 
            l.type, 
            il.qty 
        FROM item_locations il
        JOIN locations l ON il.id_location = l.id_location
        WHERE il.id_item = %s AND il.qty > 0
        ORDER BY il.qty DESC;
        """
        conn = get_connection()
        results = []
        try:
            cur = conn.cursor()
            cur.execute(sql, (id_item,))
            rows = cur.fetchall()
            for row in rows:
                results.append({
                    "id_location": row[0],
                    "code": row[1],
                    "type": row[2],
                    "qty": row[3]
                })
            return results
        except Exception as e:
            raise e
        finally:
            cur.close()
            conn.close()

    def __repr__(self):
        return f"<ItemLocation Item:{self.id_item} Loc:{self.id_location} Qty:{self.qty}>"
