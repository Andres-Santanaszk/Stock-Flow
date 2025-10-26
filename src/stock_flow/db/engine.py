import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carga variables del .env en la raíz del proyecto
load_dotenv()

PGUSER = os.getenv("PGUSER", "Andres")
PGPASSWORD = os.getenv("PGPASSWORD", "")
PGDATABASE = os.getenv("PGDATABASE", "stockflow")
PGPORT = os.getenv("PGPORT", "5432")
PGHOST = os.getenv("PGHOST", "localhost")   

DATABASE_URL = f"postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"

# ESTE nombre es el que espera create_db.py
engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)
