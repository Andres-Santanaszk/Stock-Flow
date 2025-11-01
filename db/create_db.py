# db/create_db.py
import psycopg2
from psycopg2 import sql, OperationalError, errors
from config.settings import (
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
)

import os
PGSUPERUSER = os.getenv("PGSUPERUSER", "postgres")
PGSUPERPASSWORD = os.getenv("PGSUPERPASSWORD", "---> CAMBIA ESTO") # Aqui cambian por la contraseña que usaron para
PGSUPERDB = os.getenv("PGSUPERDB", "postgres")              # la instalacion de postgres


def ensure_role():
    print(f"Verificando rol '{DB_USER}' ...")
    conn = None
    try:
        conn = psycopg2.connect(
            user=PGSUPERUSER,
            password=PGSUPERPASSWORD,
            dbname=PGSUPERDB,
            host=DB_HOST,
            port=DB_PORT,
        )
        # CREATE ROLE/ALTER ROLE sí pueden ir en transacción, no necesitas autocommit aquí.
        with conn, conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_roles WHERE rolname = %s;", (DB_USER,))
            exists = cur.fetchone() is not None

            if not exists:
                # CREATE ROLE <identificador> WITH LOGIN PASSWORD %s
                cur.execute(
                    sql.SQL("CREATE ROLE {} WITH LOGIN PASSWORD %s").format(
                        sql.Identifier(DB_USER)
                    ),
                    (DB_PASSWORD,),
                )
                # ALTER ROLE <identificador> CREATEDB
                cur.execute(
                    sql.SQL("ALTER ROLE {} CREATEDB").format(
                        sql.Identifier(DB_USER)
                    )
                )
                print(f"Rol '{DB_USER}' creado y con CREATEDB.")
            else:
                print(f"Rol '{DB_USER}' ya existe.")
    except OperationalError as e:
        print(f"Error de conexión al crear rol: {e}")
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
                print(f"DB '{DB_NAME}' ya existe.")
                return
            cur.execute(sql.SQL("CREATE DATABASE {} OWNER {}")
                        .format(sql.Identifier(DB_NAME),
                                sql.Identifier(DB_USER)))
            print(f"DB '{DB_NAME}' creada correctamente y asignada a '{DB_USER}'.")
    except OperationalError as e:
        print(f"Error de conexión al crear DB: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    ensure_role()
    ensure_database()
