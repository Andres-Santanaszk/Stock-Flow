CREATE TABLE IF NOT EXISTS items (
  id_item       SERIAL PRIMARY KEY,
  name          VARCHAR(120) NOT NULL,
  sku           VARCHAR(64)  NOT NULL UNIQUE,
  barcode       VARCHAR(32)  UNIQUE,
  brand_id      INT           REFERENCES brands(id_brand) ON DELETE SET NULL,
  description   TEXT NOT NULL DEFAULT '',
  type          item_type    NOT NULL DEFAULT 'finished_product',
  pack_type     item_pack_type NOT NULL DEFAULT 'unit',
  max_capacity  NUMERIC(18,3) NOT NULL DEFAULT 0,
  active        BOOLEAN       NOT NULL DEFAULT TRUE,
  created_at    TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_items_name ON items (name);
CREATE INDEX IF NOT EXISTS ix_items_brand_id ON items (brand_id);

-- Trigger para updated_at
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'set_updated_at') THEN
    CREATE OR REPLACE FUNCTION set_updated_at() RETURNS TRIGGER AS $f$
    BEGIN
      NEW.updated_at := NOW();
      RETURN NEW;
    END;
    $f$ LANGUAGE plpgsql;
  END IF;
END$$;

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger WHERE tgname = 'trg_items_set_updated_at'
  ) THEN
    CREATE TRIGGER trg_items_set_updated_at
      BEFORE UPDATE ON items
      FOR EACH ROW EXECUTE FUNCTION set_updated_at();
  END IF;
END$$;

-- CONTAINERS
CREATE TABLE IF NOT EXISTS containers (
  id_container SERIAL PRIMARY KEY,
  type container_type NOT NULL,    -- Rack / Shelf / Pallet / etc.
  code VARCHAR(64) NOT NULL UNIQUE, -- identificador único, corto y visible
  description TEXT,                 -- texto opcional
  active BOOLEAN NOT NULL DEFAULT TRUE
);


CREATE TABLE IF NOT EXISTS item_containers (
  id           BIGSERIAL PRIMARY KEY,
  id_item      INT NOT NULL REFERENCES items(id_item) ON DELETE RESTRICT,
  id_container INT NOT NULL REFERENCES containers(id_container) ON DELETE RESTRICT,
  location     VARCHAR(64) NOT NULL,
  qty          NUMERIC(18,3) NOT NULL DEFAULT 0 CHECK (qty >= 0),
  CONSTRAINT uq_item_containers_container_location UNIQUE (id_container, location)
);

CREATE INDEX IF NOT EXISTS ix_item_containers_item ON item_containers (id_item);
CREATE INDEX IF NOT EXISTS ix_item_containers_container ON item_containers (id_container);
CREATE INDEX IF NOT EXISTS ix_item_containers_item_container ON item_containers (id_item, id_container);

CREATE TABLE IF NOT EXISTS movements (
  id_mov      BIGSERIAL PRIMARY KEY,
  id_item     INT  NOT NULL REFERENCES items(id_item) ON DELETE RESTRICT,
  id_user     INT  NOT NULL REFERENCES users(id_user) ON DELETE RESTRICT,
  type        mov_type  NOT NULL,
  qty         NUMERIC(18,3) NOT NULL CHECK (qty <> 0),
  created_at  TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
  reason      mov_reason    NOT NULL,
  from_container_id INT REFERENCES containers(id_container),
  from_location     VARCHAR(64),
  to_container_id   INT REFERENCES containers(id_container),
  to_location       VARCHAR(64),

  CONSTRAINT chk_type_reason_consistency CHECK (
    (type = 'IN'  AND reason IN ('return_in','transfer_in','manufacture_produce')) OR
    (type = 'OUT' AND reason IN ('shipping','return_out','transfer_out','manufacture_consume')) OR
    (type = 'ADJUST' AND reason IN ('scrap','damage','relocation'))
  ),

  CONSTRAINT chk_mov_qty_sign CHECK (
    (type = 'IN'  AND qty > 0) OR
    (type = 'OUT' AND qty < 0) OR
    (type = 'ADJUST')
  ),

  CONSTRAINT chk_mov_locations_by_type CHECK (
    (type = 'IN'
      AND to_container_id IS NOT NULL AND to_location IS NOT NULL
      AND from_container_id IS NULL AND from_location IS NULL)
    OR
    (type = 'OUT'
      AND from_container_id IS NOT NULL AND from_location IS NOT NULL
      AND to_container_id IS NULL AND to_location IS NULL)
    OR
    (type = 'ADJUST' AND (
        (from_container_id IS NOT NULL AND from_location IS NOT NULL
         AND to_container_id IS NULL AND to_location IS NULL)
      OR
        (to_container_id IS NOT NULL AND to_location IS NOT NULL
         AND from_container_id IS NULL AND from_location IS NULL)
    ))
  ),

  CONSTRAINT chk_from_to_diff CHECK (
    NOT (
      from_container_id IS NOT NULL AND to_container_id IS NOT NULL
      AND from_container_id = to_container_id
      AND COALESCE(from_location,'') = COALESCE(to_location,'')
    )
  )
);


CREATE INDEX IF NOT EXISTS ix_movements_item_created_at ON movements (id_item, created_at);
CREATE INDEX IF NOT EXISTS ix_movements_created_at ON movements (created_at);
CREATE INDEX IF NOT EXISTS ix_movements_user ON movements (id_user);

