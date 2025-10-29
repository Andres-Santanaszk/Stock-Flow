import psycopg2
conn = psycopg2.connect(
    user="dev_user",
    password="temp12345",
    dbname="stockflow_db",
    host="localhost",
    port=5432
)
cur = conn.cursor()
cur.execute("SELECT version();")
print(cur.fetchone())
cur.close()
conn.close()