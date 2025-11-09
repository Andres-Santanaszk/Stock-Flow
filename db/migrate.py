import os
import psycopg2
from config.settings import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

SQL_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_FILES = [
    "001_enums.sql",
    "002_users_roles.sql",
    "003_catalogs.sql",
    "004_inventory.sql",
]

SEED_FILE = "999_seed.sql" 

def run_sql_file(conn, path):
    with open(path, "r", encoding="utf-8") as f, conn.cursor() as cur:
        sql_text = f.read()
        cur.execute(sql_text)

def migrate(load_seed=True):
    conn = psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME,   
        host=DB_HOST,
        port=DB_PORT,
        connect_timeout=5,
        options="-c client_min_messages=WARNING",
    )
    try:
        for fname in DEFAULT_FILES:
            path = os.path.join(SQL_DIR, fname)
            if not os.path.exists(path):
                raise FileNotFoundError(f"No se encontró {path}")
            print(f"Ejecutando {fname} ...")
            conn.autocommit = False
            try:
                run_sql_file(conn, path)
                conn.commit()
                print(f"OK {fname}")
            except Exception as e:
                conn.rollback()
                print(f"ERROR en {fname}: {e}")
                raise

        if load_seed:
            seed_path = os.path.join(SQL_DIR, SEED_FILE)
            if os.path.exists(seed_path):
                print(f"Ejecutando {SEED_FILE} ...")
                conn.autocommit = False
                try:
                    run_sql_file(conn, seed_path)
                    conn.commit()
                    print(f"OK {SEED_FILE}")
                except Exception as e:
                    conn.rollback()
                    print(f"ERROR en {SEED_FILE}: {e}")
                    raise
    finally:
        conn.close()


if __name__ == "__main__":
    load_seed = os.getenv("LOAD_SEED", "on").lower() in ("1", "true", "on", "yes")
    migrate(load_seed=load_seed)
