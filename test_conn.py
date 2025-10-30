import psycopg2
from db.connection import get_connection

conn = get_connection()

cur = conn.cursor()
cur.execute("SELECT version();")
print(cur.fetchone())
cur.close()
conn.close()