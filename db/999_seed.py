# db/999_seeds.py
import os
from db.connection import get_connection

def seed_roles_permissions(cur):
    cur.execute("""
    INSERT INTO roles (id, name, description) VALUES
      (1,'admin','Administrador'),
      (2,'operator','Operador de almacén'),
      (3,'viewer','Solo lectura')
    ON CONFLICT (id) DO UPDATE
      SET name = EXCLUDED.name,
          description = EXCLUDED.description;
    """)

    cur.execute("""
    INSERT INTO permissions (id, code, description) VALUES
      (1,'items.read','Puede ver items'),
      (2,'items.write','Puede crear/editar items'),
      (3,'movements.post','Puede registrar movimientos'),
      (4,'users.manage','Puede administrar usuarios')
    ON CONFLICT (id) DO UPDATE
      SET code = EXCLUDED.code,
          description = EXCLUDED.description;
    """)

    cur.execute("""
    INSERT INTO role_permissions (role_id, permission_id) VALUES
      (1,1),(1,2),(1,3),(1,4),
      (2,1),(2,2),(2,3),
      (3,1)
    ON CONFLICT DO NOTHING;
    """)

def seed_users(cur):
    cur.execute("""
    INSERT INTO users (id_user, full_name, email, password_hash, active, role_id) VALUES
      (1,'Admin','admin@example.com','$2b$12$secrethash...',TRUE,1),
      (2,'Operador','op@example.com','$2b$12$secrethash...',TRUE,2)
    ON CONFLICT (id_user) DO UPDATE
      SET full_name = EXCLUDED.full_name,
          email = EXCLUDED.email,
          password_hash = EXCLUDED.password_hash,
          active = EXCLUDED.active,
          role_id = EXCLUDED.role_id;
    """)

def seed_brands(cur):
    cur.execute("""
    INSERT INTO brands (id_brand, name, description, website, contact_email) VALUES
      (1,'Acme','Línea general','https://acme.test','info@acme.test'),
      (2,'Globex','Importaciones','https://globex.test','contact@globex.test')
    ON CONFLICT (id_brand) DO UPDATE
      SET name = EXCLUDED.name,
          description = EXCLUDED.description,
          website = EXCLUDED.website,
          contact_email = EXCLUDED.contact_email;
    """)

def seed_categories(cur):
    cur.execute("""
    INSERT INTO categories (id_category, name, class, description, active) VALUES
      (1,'Bebidas','finished_product','Bebidas listas', TRUE),
      (2,'Insumos','raw_material','Materia prima', TRUE)
    ON CONFLICT (id_category) DO UPDATE
      SET name = EXCLUDED.name,
          class = EXCLUDED.class,
          description = EXCLUDED.description,
          active = EXCLUDED.active;
    """)

def seed_containers(cur):
    cur.execute("""
    INSERT INTO containers (id_container, type, code, description, active) VALUES
      (1,'Rack','RACK-A','Rack principal', TRUE),
      (2,'Shelf','SHELF-01','Estante 1', TRUE),
      (3,'Bin','BIN-01','Bandeja 1', TRUE)
    ON CONFLICT (id_container) DO UPDATE
      SET type = EXCLUDED.type,
          code = EXCLUDED.code,
          description = EXCLUDED.description,
          active = EXCLUDED.active;
    """)

def seed_items(cur):
    # pack_type ajustado a ENUM actualizado
    cur.execute("""
    INSERT INTO items (id_item, name, sku, barcode, brand_id, description, category_id, pack_type, active) VALUES
      (1,'Refresco Cola 600ml','SKU-REF-600','1234567890123',1,'Bebida con gas',1,'bottle',TRUE),
      (2,'Azúcar KG','SKU-AZU-1K','0001112223334',2,'Saco azúcar',2,'bag',TRUE)
    ON CONFLICT (id_item) DO UPDATE
      SET name = EXCLUDED.name,
          sku = EXCLUDED.sku,
          barcode = EXCLUDED.barcode,
          brand_id = EXCLUDED.brand_id,
          description = EXCLUDED.description,
          category_id = EXCLUDED.category_id,
          pack_type = EXCLUDED.pack_type,
          active = EXCLUDED.active;
    """)

def seed_item_locations(cur):
    # qty ahora INT (ya lo era)
    cur.execute("""
    INSERT INTO item_containers (id_item, id_container, location, qty) VALUES
      (1,1,'A1',10),
      (1,2,'SHELF-01-1',5),
      (2,3,'BIN-01-1',20)
    ON CONFLICT (id_container, location) DO UPDATE
      SET qty = EXCLUDED.qty
    WHERE item_containers.id_item = EXCLUDED.id_item;
    """)

def seed_demo_movements(cur):
    cur.execute("""
    INSERT INTO movements
      (id_item, id_user, type, qty, reason, to_container_id, to_location)
    VALUES
      (1, 1, 'IN',  10, 'purchase', 1, 'A1')
    ON CONFLICT DO NOTHING;
    """)

    cur.execute("""
    INSERT INTO movements
      (id_item, id_user, type, qty, reason, from_container_id, from_location)
    VALUES
      (1, 1, 'OUT', -3, 'sale', 2, 'SHELF-01-1')
    ON CONFLICT DO NOTHING;
    """)

    cur.execute("""
    INSERT INTO movements
      (id_item, id_user, type, qty, reason, to_container_id, to_location)
    VALUES
      (2, 2, 'ADJUST', 5, 'relocation', 3, 'BIN-01-1')
    ON CONFLICT DO NOTHING;
    """)

def run(load_demo=False):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                seed_roles_permissions(cur)
                seed_users(cur)
                seed_brands(cur)
                seed_categories(cur)
                seed_containers(cur)
                seed_items(cur)
                seed_item_locations(cur)
                if load_demo:
                    seed_demo_movements(cur)
        print("✅ 999_seeds.py ejecutado correctamente.")
    finally:
        conn.close()

if __name__ == "__main__":
    load_demo = os.getenv("LOAD_DEMO_SEEDS", "off").lower() in ("1","true","on","yes")
    run(load_demo=load_demo)
