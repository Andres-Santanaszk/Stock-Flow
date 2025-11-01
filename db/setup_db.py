# db/setup_db.py
from db.create_db import ensure_database, ensure_role
from db.migrate import migrate
import os

if __name__ == "__main__":
    ensure_role()
    ensure_database()
    load_seed = os.getenv("LOAD_SEED", "on").lower() in ("1", "true", "on", "yes")
    migrate(load_seed=load_seed)
