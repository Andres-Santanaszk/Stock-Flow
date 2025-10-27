-- ENUMS base
DO $$ BEGIN
  CREATE TYPE mov_type AS ENUM ('IN', 'OUT', 'ADJUST');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE container_type AS ENUM ('Rack', 'Shelf', 'Bin', 'Pallet', 'ScrapArea', 'Cart');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE item_type AS ENUM ('finished_product', 'raw_material', 'component', 'consumable');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE uom_type AS ENUM ('Quantity', 'Weight', 'Volume', 'Length', 'Area', 'Time');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
  CREATE TYPE mov_reason AS ENUM (
    'purchase', 'sale', 'return_in', 'return_out', 'scrap', 'damage',
    'transfer_in', 'transfer_out', 'manufacture_consume', 'manufacture_produce'
  );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
