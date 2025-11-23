import psycopg2
from psycopg2 import OperationalError
from config.settings import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT

def get_connection():
    try:
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME,
            host=DB_HOST,
            port=DB_PORT,
            connect_timeout=5,
            options='-c statement_timeout=5000'
        )
        return conn
    except OperationalError as e:
        print("Error de conexión a la base de datos:", e)
        raise
