# db/999_seeds.py
import os
from db.connection import get_connection

def seed_roles_permissions(cur):
    cur.execute("""
    INSERT INTO roles (id, name, description) VALUES
      (1, 'Administrador', 'Acceso total al sistema'),
      (2, 'Líder de Almacén', 'Gestiona operaciones de almacén'),
      (3, 'Recursos Humanos', 'Alta y administración de usuarios'),
      (4, 'Operador de Almacén', 'Ejecuta movimientos de inventario')
    ON CONFLICT (id) DO UPDATE
      SET name = EXCLUDED.name,
          description = EXCLUDED.description;
    """)

    cur.execute("""
    INSERT INTO permissions (id, code, description) VALUES
      (1, 'items.read', 'Puede ver ítems del inventario'),
      (2, 'items.write', 'Puede crear o editar ítems'),
      (3, 'movements.post', 'Puede registrar movimientos de inventario'),
      (4, 'users.manage', 'Puede administrar usuarios y roles'),
      (5, 'inventory.view', 'Puede ver el estado del inventario'),
      (6, 'locations.view', 'Puede ver ubicaciones'),
      (7, 'reports.view', 'Puede acceder al historial de movimientos'),
      (8, 'catalogs.manage', 'Puede gestionar catálogos base (marcas, categorías, etc.)')
    ON CONFLICT (id) DO UPDATE
      SET code = EXCLUDED.code,
          description = EXCLUDED.description;
    """)

    cur.execute("""
    INSERT INTO role_permissions (role_id, permission_id) VALUES
      (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),
      (2,1),(2,2),(2,3),(2,5),(2,6),(2,7),
      (3,4),
      (4,1),(4,3),(4,5),(4,6)
    ON CONFLICT DO NOTHING;
    """)

def seed_users(cur):
    cur.execute("""
    INSERT INTO users (id_user, full_name, email, password_hash, active, role_id) VALUES
      (1,'Admin','admin@demo.com','$2b$12$secrethash...',TRUE,1),
      (2,'Operador','operador@demo.com','$2b$12$secrethash...',TRUE,2)
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
      (1,'Uline','Equipamiento industrial y de almacén','https://www.uline.com','sales@uline.com'),
      (2,'Dewalt','Herramientas eléctricas profesionales','https://www.dewalt.com','info@dewalt.com'),
      (3,'Milwaukee','Herramientas industriales','https://www.milwaukeetool.com','support@milwaukeetool.com'),
      (4,'3M','Productos de seguridad y adhesivos','https://www.3m.com','contact@3m.com')
    ON CONFLICT (id_brand) DO UPDATE
      SET name = EXCLUDED.name,
          description = EXCLUDED.description,
          website = EXCLUDED.website,
          contact_email = EXCLUDED.contact_email;
    """)

def seed_categories(cur):
    # Usa SOLO valores válidos del enum item_class: finished_product, raw_material, component, consumable
    cur.execute("""
    INSERT INTO categories (id_category, name, class, description, active) VALUES
      (1,'Equipo de Protección','consumable','Guantes, cascos, gafas, etc.', TRUE),
      (2,'Herramientas','component','Herramientas eléctricas y manuales', TRUE),
      (3,'Empaque','consumable','Cajas, cintas, etiquetas y materiales de embalaje', TRUE)
    ON CONFLICT (id_category) DO UPDATE
      SET name = EXCLUDED.name,
          class = EXCLUDED.class,
          description = EXCLUDED.description,
          active = EXCLUDED.active;
    """)

def seed_locations(cur):
    # Usa SOLO valores válidos del enum location_type: Rack, Shelf, Bin, Pallet, ScrapArea, Cart
    cur.execute("""
    INSERT INTO locations (id_location, type, code, description, active) VALUES
      (1,'Rack','RACK-A1','Rack A1 principal', TRUE),
      (2,'Rack','RACK-B2','Rack B2 secundario', TRUE),
      (3,'Bin','BIN-01','Bandeja de picking 01', TRUE),
      (4,'Cart','STAGE-OUT','Carro de embarque', TRUE),
      (5,'Cart','STAGE-IN','Carro de recepción', TRUE)
    ON CONFLICT (id_location) DO UPDATE
      SET type = EXCLUDED.type,
          code = EXCLUDED.code,
          description = EXCLUDED.description,
          active = EXCLUDED.active;
    """)

def seed_items(cur):
    cur.execute("""
    INSERT INTO items (id_item, name, sku, barcode, brand_id, description, category_id, pack_type, min_qty, active) VALUES
      (1,'Guantes de Nitrilo XL','SKU-GUA-001','1234567890123',4,'Guantes resistentes para manipulación industrial',1,'box', 50, TRUE),
      (2,'Taladro Inalámbrico 20V','SKU-TAL-020','1234567890456',2,'Taladro con batería de litio',2,'unit', 5, TRUE),
      (3,'Cinta de Embalaje 48mm','SKU-CIN-048','1234567890789',1,'Cinta adhesiva industrial',3,'roll', 20, TRUE),
      (4,'Lentes de Seguridad Transparentes','SKU-LEN-003','1234567891123',4,'Protección ocular estándar',1,'unit', 15, TRUE)
    ON CONFLICT (id_item) DO UPDATE
      SET name = EXCLUDED.name,
          sku = EXCLUDED.sku,
          barcode = EXCLUDED.barcode,
          brand_id = EXCLUDED.brand_id,
          description = EXCLUDED.description,
          category_id = EXCLUDED.category_id,
          pack_type = EXCLUDED.pack_type,
          min_qty = EXCLUDED.min_qty,
          active = EXCLUDED.active;
    """)


def seed_demo_movements(cur):
    # IN: entradas de compra (qty positiva; el trigger ya deja el signo correcto)
    cur.execute("""
    INSERT INTO movements (id_item, id_user, type, reason, qty, to_location_id)
    VALUES
      (1, 1, 'IN', 'purchase', 100, 5),
      (2, 1, 'IN', 'purchase',  20, 5),
      (3, 1, 'IN', 'purchase',  50, 2),
      (4, 1, 'IN', 'purchase',  40, 3)
    ON CONFLICT DO NOTHING;
    """)

    # OUT: salidas por venta
    cur.execute("""
    INSERT INTO movements (id_item, id_user, type, reason, qty, from_location_id)
    VALUES
      (3, 2, 'OUT', 'sale', 10, 2),
      (2, 2, 'OUT', 'sale',  5, 5)
    ON CONFLICT DO NOTHING;
    """)

    # ADJUST: ajuste negativo por daño
    cur.execute("""
    INSERT INTO movements (id_item, id_user, type, reason, qty, from_location_id)
    VALUES
      (1, 1, 'ADJUST', 'damage', 5, 5)
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
                seed_locations(cur)
                seed_items(cur)
                if load_demo:
                    seed_demo_movements(cur)
        print("999_seeds.py ejecutado correctamente.")
    finally:
        conn.close()

if __name__ == "__main__":
    load_demo = os.getenv("LOAD_DEMO_SEEDS", "on").lower() in ("1","true","on","yes")
    run(load_demo=load_demo)
