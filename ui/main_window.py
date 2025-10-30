# ui/main_window.py
from db.connection import get_connection
def test_query():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT NOW();")
                print("✅ Conectado:", cur.fetchone())
    except Exception as e:
        print("❌ Error:", e)

test_query()