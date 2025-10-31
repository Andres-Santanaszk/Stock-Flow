# db/create_db.py
import psycopg2
from psycopg2 import sql
from config.settings import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

def ensure_database():
    conn = psycopg2.connect(
        user="postgres",
        password="Falcored94", # aqui tienen que cambiar a la password que pusieron al momento de instalar postgres 
        dbname="postgres",
        host=DB_HOST,
        port=DB_PORT,
    )
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname=%s;", (DB_NAME,))
            exists = cur.fetchone() is not None
            if exists:
                print(f"DB '{DB_NAME}' ya existe.")
                return

            cur.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME))
            )
            print(f"DB '{DB_NAME}' creada correctamente.")
    finally:
        conn.close()

if __name__ == "__main__":
    ensure_database()
