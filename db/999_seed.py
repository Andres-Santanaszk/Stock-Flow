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
    cur.execute("""
    INSERT INTO locations (id_location, type, code, description, active) VALUES
      (1,'Rack','RACK-A1','Rack A1 principal', TRUE),
      (2,'Rack','RACK-B2','Rack B2 secundario', TRUE),
      (3,'Bin','BIN-01','Bandeja de picking 01', TRUE),
      (4,'Cart','STAGE-OUT','Carro de embarque', TRUE),
      (5,'Cart','STAGE-IN','Carro de recepción', TRUE),
      (6,'ScrapArea','SCRAP-ZONE','Área temporal de desecho/merma', TRUE),
      (7,'Rack','RACK-C1','Rack C1 herramientas eléctricas', TRUE),
      (8,'Rack','RACK-D1','Rack D1 refacciones pesadas', TRUE),
      (9,'Shelf','SHELF-A1','Estante A1 consumibles generales', TRUE),
      (10,'Shelf','SHELF-A2','Estante A2 equipo de protección personal', TRUE),
      (11,'Bin','BIN-02','Bandeja de tornillería fina', TRUE),
      (12,'Bin','BIN-03','Bandeja de conectores eléctricos', TRUE),
      (13,'Pallet','PALLET-Z1','Tarima zona alta Z1 materiales voluminosos', TRUE),
      (14,'Pallet','PALLET-Z2','Tarima zona alta Z2 materiales a granel', TRUE),
      (15,'ScrapArea','SCRAP-METAL','Zona de chatarra metálica', TRUE),
      (16,'Cart','MOVE-01','Carro móvil interno 01', TRUE)
    ON CONFLICT (id_location) DO UPDATE
      SET type = EXCLUDED.type,
          code = EXCLUDED.code,
          description = EXCLUDED.description,
          active = EXCLUDED.active;
    """)


def seed_items(cur):
    cur.execute("""
    INSERT INTO items (id_item, name, sku, barcode, brand_id, description, category_id, pack_type, min_qty, active) VALUES
      (1,'Guantes de Nitrilo XL','GUA-001','1234567890123',4,'Guantes resistentes para manipulación industrial',1,'box', 50, TRUE),
      (2,'Taladro Inalámbrico 20V','TAL-020','1234567890456',2,'Taladro con batería de litio',2,'unit', 2, TRUE),                       -- BAJO
      (3,'Cinta de Embalaje 48mm','CIN-048','1234567890789',1,'Cinta adhesiva industrial',3,'roll', 20, TRUE),
      (4,'Lentes de Seguridad Transparentes','LEN-003','1234567891123',4,'Protección ocular estándar',1,'unit', 10, TRUE),

      -- Nuevos ítems industriales (ajustados)
      (5,'Casco de Seguridad Industrial','CAS-001','1234567891456',4,'Casco con suspensión de 4 puntos',1,'unit', 5, TRUE),
      (6,'Botas de Seguridad con Punta de Acero','BOT-001','1234567891789',4,'Calzado de seguridad antiderrapante',1,'unit', 4, TRUE),
      (7,'Mascarilla Respirador P95','RES-095','1234567892123',4,'Respirador para partículas industriales',1,'box', 20, TRUE),
      (8,'Juego de Llaves Combinadas 10pz','LLA-010','1234567892456',2,'Juego de llaves para mantenimiento mecánico',2,'box', 1, TRUE),   -- BAJO
      (9,'Juego de Dados de Impacto 1/2"','DAD-IMP','1234567892789',2,'Dados para pistola de impacto',2,'box', 1, TRUE),                 -- BAJO
      (10,'Disco de Corte 4-1/2" Inox','DIS-INOX','1234567893123',1,'Discos para esmeriladora angular acero/inox',3,'box', 25, TRUE),
      (11,'Grasa Multiusos Cartucho','GRA-001','1234567893456',1,'Grasa para lubricación general de maquinaria',3,'box', 4, TRUE),       -- BAJO
      (12,'Aceite Hidráulico ISO 46','ACE-H46','1234567893789',3,'Aceite para sistemas hidráulicos industriales',3,'unit', 1, TRUE),     -- MUY BAJO
      (13,'Silicón Sellador Alta Temperatura','SIL-HT','1234567894123',3,'Sellador para bridas y juntas en equipos',3,'box', 3, TRUE),   -- BAJO
      (14,'Cinta Aislante Negra','CIN-AIS','1234567894456',1,'Cinta para aislamiento eléctrico general',3,'roll', 30, TRUE)
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



def seed_item_locations(cur):
    cur.execute("""
    INSERT INTO item_locations (id_item, id_location, qty) VALUES
      -- Originales / Stock bueno
      (1, 5, 0),
      (2, 5, 0),
      (3, 2, 0),
      (4, 3, 0),
      (1, 2, 0),
      (2, 1, 3),   -- Taladro en RACK-A1
      (2, 8, 1),   -- Taladro en RACK-D1 refacciones pesadas
      (3, 9, 25),  -- Cinta de embalaje en SHELF-A1 consumibles
      (5, 10, 6),  -- Cascos en SHELF-A2 EPP
      (6, 10, 4),  -- Botas de seguridad en SHELF-A2 EPP
      (7, 9, 10),  -- Respiradores en SHELF-A1 consumibles
      (8, 7, 2),   -- Llaves combinadas en RACK-C1 herramientas eléctricas
      (10, 11, 40),-- Discos de corte en BIN-02 tornillería/discos
      (11, 16, 8), -- Grasa multiusos en carrito interno
      (12, 13, 1), -- Aceite hidráulico en PALLET-Z1

      -- ITEMS EN SCRAP / MERMA (Usando ID 6 que definimos como ScrapArea)
      (1, 6, 5),   -- 5 Cajas de Guantes dañadas
      (3, 6, 1),   -- 1 Rollo de cinta aplastado
      (5, 6, 2)    -- 2 Cascos rotos
    ON CONFLICT DO NOTHING;
    """)

def seed_demo_movements(cur):
    cur.execute("""
    INSERT INTO movements (id_item, id_user, type, reason, qty, to_location_id)
    VALUES
      (1, 1, 'IN', 'purchase', 100, 5),
      (2, 1, 'IN', 'purchase',  20, 5),
      (3, 1, 'IN', 'purchase',  50, 2),
      (4, 1, 'IN', 'purchase',  40, 3)
    ON CONFLICT DO NOTHING;
    """)

    cur.execute("""
    INSERT INTO movements (id_item, id_user, type, reason, qty, from_location_id)
    VALUES
      (3, 2, 'OUT', 'sale', 10, 2),
      (2, 2, 'OUT', 'sale',  5, 5)
    ON CONFLICT DO NOTHING;
    """)

    cur.execute("""
    INSERT INTO movements (id_item, id_user, type, reason, qty, from_location_id)
    VALUES
      (1, 1, 'ADJUST', 'damage', 5, 5)
    ON CONFLICT DO NOTHING;
    """)
    
    cur.execute("""
    INSERT INTO movements (id_item, id_user, type, reason, qty, from_location_id, to_location_id)
    VALUES
      (1, 1, 'ADJUST', 'relocation', 10, 5, 2)
    ON CONFLICT DO NOTHING;
    """)

def sync_all_sequences(cur):
    tables_with_sequences = [
        ('roles', 'id'),
        ('permissions', 'id'),
        ('users', 'id_user'),
        ('brands', 'id_brand'),
        ('categories', 'id_category'),
        ('locations', 'id_location'),
        ('items', 'id_item'),
        ('movements', 'id_mov') 
    ]
    
    for table, id_col in tables_with_sequences:
        seq_name = f"{table}_{id_col}_seq"
        sql = f"""
        SELECT setval(
            '{seq_name}', 
            COALESCE((SELECT MAX({id_col}) FROM {table}), 0) + 1, 
            false
        );
        """
        try:
            cur.execute(sql)
        except Exception as e:
            pass

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
                seed_item_locations(cur)
                
                if load_demo:
                    seed_demo_movements(cur)
                
                sync_all_sequences(cur) 
                
        print("999_seeds.py ejecutado correctamente.")
    finally:
        conn.close()

if __name__ == "__main__":
    load_demo = os.getenv("LOAD_DEMO_SEEDS", "on").lower() in ("1","true","on","yes")
    run(load_demo=load_demo)