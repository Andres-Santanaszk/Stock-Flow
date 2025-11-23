from connection import get_connection


#nosotros no tenemos productos, es simplemente un ejemplo.
def get_products():
    try:
        conn = get_connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, nombre, precio FROM productos;")
                rows = cur.fetchall()
                return rows
    except Exception as e:
        print("Error consultando productos:", e)
        return []
    finally:
        if conn:
            conn.close()
