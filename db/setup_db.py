# db/setup_db.py
import os
import importlib.util
from db.create_db import ensure_database, ensure_role
from db.migrate import migrate

def run_python_seed_by_path(seed_path: str, load_demo: bool):
    if not os.path.exists(seed_path):
        print(f"Seed Python no encontrada: {seed_path}")
        return
    spec = importlib.util.spec_from_file_location("db_seed_module", seed_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  
    if not hasattr(mod, "run"):
        raise RuntimeError(f"{seed_path} no define la función run(load_demo=...)")
    mod.run(load_demo=load_demo)

if __name__ == "__main__":
    # 1) Bootstrap de rol y DB
    ensure_role()
    ensure_database()

    # 2) Migraciones
    load_seed = os.getenv("LOAD_SEED", "on").lower() in ("1", "true", "on", "yes")
    migrate(load_seed=load_seed)  # esto sigue ejecutando 999_seed.sql si existe

    # 3) Seeds en Python (db/999_seed.py)
    if load_seed:
        load_demo = os.getenv("LOAD_DEMO_SEEDS", "off").lower() in ("1", "true", "on", "yes")
        seed_path = os.path.join(os.path.dirname(__file__), "999_seed.py")
        print("\n▶ Ejecutando 999_seed.py ...")
        run_python_seed_by_path(seed_path, load_demo=load_demo)
        print("✔ Seeds Python ejecutadas correctamente.")
