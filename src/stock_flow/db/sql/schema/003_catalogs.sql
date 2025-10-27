-- BRANDS (marcas)
CREATE TABLE IF NOT EXISTS brands (
  id_brand     SERIAL PRIMARY KEY,
  name         VARCHAR(120)  NOT NULL UNIQUE,
  description  TEXT,
  website      VARCHAR(255),            -- URL corta típica
  contact_email VARCHAR(254),           -- email de contacto
  created_at   TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

-- UOM (unidades de medida)
CREATE TABLE IF NOT EXISTS uom (
  id_uom   SERIAL PRIMARY KEY,
  name     VARCHAR(80)  NOT NULL UNIQUE,  -- "Kilogramo", "Unidad", etc.
  symbol   VARCHAR(16)  NOT NULL UNIQUE,  -- "kg", "un", "mL"
  type     uom_type     NOT NULL
);
