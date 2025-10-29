-- ITEMS
CREATE TABLE IF NOT EXISTS items (
  id_item       SERIAL PRIMARY KEY,
  name          VARCHAR(180) NOT NULL,         -- nombre de producto/insumo
  sku           VARCHAR(64)  NOT NULL UNIQUE,  -- código interno
  barcode       VARCHAR(32)  UNIQUE,           -- más flexible que 14 (EAN/UPC)
  type          item_type    NOT NULL DEFAULT 'finished_product',
  item_qty      NUMERIC(18,3) NOT NULL DEFAULT 0,  -- snapshot total (monobodega)
  min_stock     NUMERIC(18,3) NOT NULL DEFAULT 0,  -- umbral para bajo stock
  max_capacity  NUMERIC(18,3) NOT NULL DEFAULT 0,  -- 0 = sin límite
  active        BOOLEAN       NOT NULL DEFAULT TRUE,
  brand_id      INT           REFERENCES brands(id_brand) ON DELETE SET NULL,
  created_at    TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

-- índice para búsquedas por nombre
CREATE INDEX IF NOT EXISTS ix_items_name ON items (name);

-- CONTAINERS (ubicaciones físicas)
CREATE TABLE IF NOT EXISTS containers (
  id_container  SERIAL PRIMARY KEY,
  type          container_type NOT NULL,   -- Rack/Shelf/Bin/Pallet/ScrapArea/Cart
  description   TEXT,
  active        BOOLEAN        NOT NULL DEFAULT TRUE
);

-- ITEMS en CONTENEDORES (una ubicación física única por fila)
CREATE TABLE IF NOT EXISTS item_containers (
  id           BIGSERIAL PRIMARY KEY,
  id_item      INT NOT NULL REFERENCES items(id_item) ON DELETE RESTRICT,
  id_container INT NOT NULL REFERENCES containers(id_container) ON DELETE RESTRICT,
  location     VARCHAR(64) NOT NULL,
  qty          NUMERIC(18,3) NOT NULL DEFAULT 0 CHECK (qty >= 0),
  CONSTRAINT uq_item_containers_container_location UNIQUE (id_container, location)
);

CREATE INDEX IF NOT EXISTS ix_item_containers_item_container
  ON item_containers (id_item, id_container);


-- UOM por ITEM (factores de conversión)
CREATE TABLE IF NOT EXISTS item_uom (
  id_item    INT NOT NULL REFERENCES items(id_item) ON DELETE CASCADE,
  id_uom    INT NOT NULL REFERENCES uom(id_uom)    ON DELETE RESTRICT,
  uom_value NUMERIC(18,6) NOT NULL CHECK (uom_value > 0),
  CONSTRAINT pk_item_uom PRIMARY KEY (id_item, id_uom)
);

CREATE INDEX IF NOT EXISTS ix_item_uom_uom ON item_uom (id_uom);

-- MOVEMENTS (Kardex)
CREATE TABLE IF NOT EXISTS movements (
  id_mov      BIGSERIAL PRIMARY KEY,
  id_item     INT       NOT NULL REFERENCES items(id_item) ON DELETE RESTRICT,
  id_user     INT       NOT NULL REFERENCES users(id_user) ON DELETE RESTRICT,
  type        mov_type  NOT NULL DEFAULT 'OUT',  -- informativo; signo lo da qty
  qty         NUMERIC(18,3) NOT NULL CHECK (qty <> 0),   -- >0 entrada, <0 salida
  created_at  TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
  reason      mov_reason    NOT NULL,
  source      VARCHAR(120),  -- "Rack-01", "Recepción", etc.
  target      VARCHAR(120)   -- "Cliente", "Scrap", "Shipping", etc.
);

-- Índices útiles para reportes por ítem y fecha
CREATE INDEX IF NOT EXISTS ix_movements_item_created_at ON movements (id_item, created_at);
CREATE INDEX IF NOT EXISTS ix_movements_created_at ON movements (created_at);
