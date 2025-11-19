CREATE TABLE IF NOT EXISTS items (
  id_item       SERIAL PRIMARY KEY,
  name          VARCHAR(120) NOT NULL,
  sku           VARCHAR(64)  NOT NULL UNIQUE,
  barcode       VARCHAR(32)  UNIQUE,
  brand_id      INT          REFERENCES brands(id_brand) ON DELETE SET NULL,
  description   TEXT NOT NULL DEFAULT '',
  category_id   INT          REFERENCES categories(id_category) ON DELETE SET NULL,
  pack_type     item_pack_type NOT NULL DEFAULT 'unit',
  min_qty       INT NOT NULL DEFAULT 0,
  active        BOOLEAN       NOT NULL DEFAULT TRUE,
  created_at    TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_items_name ON items (name);
CREATE INDEX IF NOT EXISTS ix_items_brand_id ON items (brand_id);

CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_timestamp
BEFORE UPDATE ON items
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

CREATE TABLE IF NOT EXISTS locations (
  id_location   SERIAL PRIMARY KEY,
  type          location_type NOT NULL, 
  code          VARCHAR(64) NOT NULL UNIQUE,
  description   TEXT,
  active        BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_locations_type ON locations(type);

CREATE TABLE IF NOT EXISTS item_locations (
  id           SERIAL PRIMARY KEY,
  id_item      INT NOT NULL REFERENCES items(id_item) ON DELETE RESTRICT,
  id_location  INT NOT NULL REFERENCES locations(id_location) ON DELETE RESTRICT,
  qty          INT NOT NULL DEFAULT 0 CHECK (qty >= 0),

  CONSTRAINT unique_item_locations UNIQUE (id_item, id_location)
);

CREATE INDEX IF NOT EXISTS ix_item_locations_item      ON item_locations (id_item);
CREATE INDEX IF NOT EXISTS ix_item_locations_location  ON item_locations (id_location);

CREATE TABLE IF NOT EXISTS movements (
  id_mov            SERIAL PRIMARY KEY,
  id_item           INT NOT NULL REFERENCES items(id_item) ON DELETE RESTRICT,
  id_user           INT NOT NULL REFERENCES users(id_user) ON DELETE RESTRICT,
  type              mov_type NOT NULL,      
  reason            mov_reason NOT NULL,    
  qty               INT NOT NULL,           
  created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  from_location_id  INT REFERENCES locations(id_location),
  to_location_id    INT REFERENCES locations(id_location),
  
  CONSTRAINT chk_qty_nonzero CHECK (qty <> 0),

  CONSTRAINT check_type_reason CHECK (
    (type = 'IN'  AND reason IN ('purchase','return_in','transfer_in','manufacture_produce')) OR
    (type = 'OUT' AND reason IN ('sale','shipping','return_out','transfer_out','manufacture_consume')) OR
    (type = 'ADJUST' AND reason IN ('scrap','damage','relocation'))
  ),

  CONSTRAINT chk_mov_locations_by_type CHECK (
    (type = 'IN' AND to_location_id IS NOT NULL AND from_location_id IS NULL)
    OR
    (type = 'OUT' AND from_location_id IS NOT NULL AND to_location_id IS NULL)
    OR
    (type = 'ADJUST' AND (from_location_id IS NOT NULL OR to_location_id IS NOT NULL))
  ),

  CONSTRAINT chk_from_to_diff CHECK (
    NOT (
      from_location_id IS NOT NULL AND to_location_id IS NOT NULL
      AND from_location_id = to_location_id
    )
  )
);

CREATE INDEX IF NOT EXISTS ix_movements_item_created_at ON movements (id_item, created_at);
CREATE INDEX IF NOT EXISTS ix_movements_created_at      ON movements (created_at);
CREATE INDEX IF NOT EXISTS ix_movements_user            ON movements (id_user);
CREATE INDEX IF NOT EXISTS ix_movements_from_loc        ON movements (from_location_id);
CREATE INDEX IF NOT EXISTS ix_movements_to_loc          ON movements (to_location_id);



CREATE OR REPLACE FUNCTION enforce_qty_sign() RETURNS TRIGGER AS $$
BEGIN
  NEW.qty := ABS(NEW.qty);

  IF NEW.type = 'IN' THEN
    NEW.qty := NEW.qty;
  ELSIF NEW.type = 'OUT' THEN
    NEW.qty := -NEW.qty;
  ELSIF NEW.type = 'ADJUST' THEN

    IF NEW.from_location_id IS NOT NULL AND NEW.to_location_id IS NOT NULL THEN
       NEW.qty := NEW.qty;
       
    ELSIF NEW.from_location_id IS NOT NULL THEN
       NEW.qty := -NEW.qty;
       
    ELSIF NEW.to_location_id IS NOT NULL THEN
       NEW.qty := NEW.qty;
       
    ELSE
       RAISE EXCEPTION 'Ajuste requiere from_location_id o to_location_id';
    END IF;

  ELSE
    RAISE EXCEPTION 'Tipo de movimiento desconocido: %', NEW.type;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_movements_sign ON movements;
CREATE TRIGGER trg_movements_sign
BEFORE INSERT OR UPDATE OF qty, type, from_location_id, to_location_id
ON movements
FOR EACH ROW
EXECUTE FUNCTION enforce_qty_sign();


CREATE OR REPLACE FUNCTION apply_movement_ins() RETURNS TRIGGER AS $$
DECLARE
  qty_abs INT;
  current_qty INT;
BEGIN
  qty_abs := ABS(NEW.qty);

  IF NEW.from_location_id IS NOT NULL THEN
    UPDATE item_locations 
       SET qty = qty - qty_abs 
     WHERE id_item = NEW.id_item 
       AND id_location = NEW.from_location_id;

    IF NOT FOUND THEN 
       RAISE EXCEPTION 'El item % no existe en la ubicación de origen %', NEW.id_item, NEW.from_location_id; 
    END IF;
    
    SELECT qty INTO current_qty FROM item_locations 
     WHERE id_item = NEW.id_item AND id_location = NEW.from_location_id;
     
    IF current_qty < 0 THEN 
       RAISE EXCEPTION 'Stock insuficiente en origen %. (Quedaría en %)', NEW.from_location_id, current_qty; 
    END IF;
  END IF;

  IF NEW.to_location_id IS NOT NULL THEN

    UPDATE item_locations 
       SET qty = qty + qty_abs 
     WHERE id_item = NEW.id_item 
       AND id_location = NEW.to_location_id;

    IF NOT FOUND THEN
      INSERT INTO item_locations (id_item, id_location, qty)
      VALUES (NEW.id_item, NEW.to_location_id, qty_abs);
    END IF;
    
  END IF;

  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_movements_apply_insert ON movements;
CREATE TRIGGER trg_movements_apply_insert
AFTER INSERT ON movements
FOR EACH ROW
EXECUTE FUNCTION apply_movement_ins();


CREATE OR REPLACE VIEW v_movements_signed AS
SELECT
  m.*,
  m.qty AS qty_signed
FROM movements m;

CREATE OR REPLACE VIEW v_stock_available AS
SELECT 
    il.id_item,
    i.sku,
    i.name AS item_name,
    i.pack_type,
    
    il.id_location,
    l.code AS location_code,
    l.type AS location_type,
    
    il.qty
FROM item_locations il
JOIN items i ON il.id_item = i.id_item
JOIN locations l ON il.id_location = l.id_location
WHERE il.qty > 0 
ORDER BY i.name ASC, il.qty DESC;
