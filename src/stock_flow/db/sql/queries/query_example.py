from db.connection import get_connection, release_connection

def get_all_inventory_items():
    conn = get_connection()  #pedir conexion al pool
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM inventory ORDER BY id;")
            rows = cur.fetchall()
            return rows
    except Exception as e:
        print("Error al obtener inventario:", e)
        return []
    finally:
        release_connection(conn)  #devolver conexion al pool
