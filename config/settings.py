import os
from dotenv import load_dotenv

DEV_ENV_FILE = ".env.development"
PROD_ENV_FILE = ".env.production"

if os.path.exists(DEV_ENV_FILE):
    env_file = DEV_ENV_FILE
elif os.path.exists(PROD_ENV_FILE):
    env_file = PROD_ENV_FILE
else:
    raise FileNotFoundError(
        "No se encontro ni .env.development ni .env.production"
    )

load_dotenv(env_file)

ENV = os.getenv("ENV", "development")

print(f"Environment loaded from {env_file} -> ENV={ENV}")
DB_USER = os.getenv("PGUSER", "dev_user")
DB_PASSWORD = os.getenv("PGPASSWORD", "temp12345")
DB_NAME = os.getenv("PGDATABASE", "stockflow")
DB_HOST = os.getenv("PGHOST", "localhost")
DB_PORT = os.getenv("PGPORT", 5432)
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")