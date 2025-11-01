DO $$ BEGIN
  CREATE TYPE mov_type AS ENUM ('IN', 'OUT', 'ADJUST');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE container_type AS ENUM ('Rack', 'Shelf', 'Bin', 'Pallet', 'ScrapArea', 'Cart');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE item_class AS ENUM ('finished_product', 'raw_material', 'component', 'consumable');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;


DO $$ BEGIN
  CREATE TYPE mov_reason AS ENUM (
    'sale', 'purchase', 'return_in', 'return_out', 'scrap', 'damage', 'shipping',
    'transfer_in', 'transfer_out', 'manufacture_consume', 'manufacture_produce', 'relocation'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE item_pack_type AS ENUM (
    'unit',        -- pieza suelta, unidad
    'package',     -- paquete pequeño
    'box',         -- caja o master pack
    'bottle',      -- botella o frasco
    'bag',         -- bolsa
    'roll',        -- rollo
    'meter',       -- longitud
    'liter',       -- volumen
    'set'          -- conjunto o kit
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

