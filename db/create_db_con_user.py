# db/create_db.py
import psycopg2
from psycopg2 import sql, OperationalError, errors
from config.settings import (
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
)

# puedes usar superusuario distinto si lo defines en .env
import os
PGSUPERUSER = os.getenv("PGSUPERUSER", "postgres")
PGSUPERPASSWORD = os.getenv("PGSUPERPASSWORD", DB_PASSWORD)
PGSUPERDB = os.getenv("PGSUPERDB", "postgres")


def ensure_role():
    """
    Crea el rol (usuario de PostgreSQL) definido en el .env si no existe.
    Usa el superusuario para conectarse.
    """
    print(f"▶ Verificando rol '{DB_USER}' ...")
    conn = None
    try:
        conn = psycopg2.connect(
            user=PGSUPERUSER,
            password=PGSUPERPASSWORD,
            dbname=PGSUPERDB,
            host=DB_HOST,
            port=DB_PORT,
        )
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = %s) THEN
                        EXECUTE format(
                            'CREATE ROLE %I WITH LOGIN PASSWORD %L',
                            %s, %s
                        );
                        EXECUTE format('ALTER ROLE %I CREATEDB;', %s);
                        RAISE NOTICE 'Rol % creado correctamente.', %s;
                    ELSE
                        RAISE NOTICE 'Rol % ya existe.', %s;
                    END IF;
                END$$;
            """, (DB_USER, DB_USER, DB_USER, DB_PASSWORD, DB_USER, DB_USER))
        print(f"✔ Rol '{DB_USER}' listo.")
    except OperationalError as e:
        print(f"❌ Error de conexión al crear rol: {e}")
    finally:
        if conn:
            conn.close()


def ensure_database():
    """
    Crea la base de datos si no existe.
    """
    print(f"▶ Verificando base '{DB_NAME}' ...")
    conn = None
    try:
        conn = psycopg2.connect(
            user=PGSUPERUSER,
            password=PGSUPERPASSWORD,
            dbname=PGSUPERDB,
            host=DB_HOST,
            port=DB_PORT,
        )
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (DB_NAME,))
            if cur.fetchone():
                print(f"✔ DB '{DB_NAME}' ya existe.")
                return
            cur.execute(sql.SQL("CREATE DATABASE {} OWNER {}")
                        .format(sql.Identifier(DB_NAME),
                                sql.Identifier(DB_USER)))
            print(f"✔ DB '{DB_NAME}' creada correctamente y asignada a '{DB_USER}'.")
    except OperationalError as e:
        print(f"❌ Error de conexión al crear DB: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    ensure_role()
    ensure_database()
