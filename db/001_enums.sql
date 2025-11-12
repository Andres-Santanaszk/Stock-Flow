CREATE TYPE mov_type AS ENUM ('IN', 'OUT', 'ADJUST');
CREATE TYPE location_type AS ENUM ('Rack', 'Shelf', 'Bin', 'Pallet', 'ScrapArea', 'Cart');
CREATE TYPE item_class AS ENUM ('finished_product', 'raw_material', 'component', 'consumable');
CREATE TYPE mov_reason AS ENUM (
    'sale', 'purchase', 'return_in', 'return_out', 'scrap', 'damage', 'shipping',
    'transfer_in', 'transfer_out', 'manufacture_consume', 'manufacture_produce', 'relocation'
  );

CREATE TYPE item_pack_type AS ENUM (
    'unit',        -- pieza suelta
    'package',     -- paquete pequeño
    'box',         -- caja o master pack
    'bottle',      -- botella o frasco
    'bag',         -- bolsa
    'roll',        -- rollo
    'set'          -- conjunto o kit
  );



