from psycopg2.pool import ThreadedConnectionPool, PoolError
from config.settings import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT

try:
    pool = ThreadedConnectionPool(
        minconn=1,
        maxconn=5,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
        connect_timeout=5
    )
    print("Pool de conexiones creado correctamente.")
except Exception as e:
    print("Error al crear el pool de conexiones:", e)
    pool = None

def get_connection():
    if pool is None:
        raise ConnectionError("Pool no inicializado.")
    try:
        return pool.getconn()
    except PoolError as e:
        print("Error: No hay conexiones libres en el pool.", e)
        raise
    
def release_connection(conn):
    """Devuelve la conexión al pool."""
    pool.putconn(conn)

def close_all_connections():
    """Cierra todas las conexiones al salir del programa."""
    pool.closeall()