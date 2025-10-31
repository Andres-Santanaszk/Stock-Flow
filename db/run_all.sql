\set ON_ERROR_STOP on
\echo -----------------------------------------
\echo Running run_all.sql on :HOST/:DB as :USER
\echo -----------------------------------------

-- 1) crea db si no existe (ejecutado contra 'postgres')
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = :'DB') THEN
    PERFORM dblink_connect('dbname=' || current_database()); -- no-op si dblink no existe
  END IF;
END$$;

-- si estás conectado ya a la DB destino, ignora lo de arriba

-- 2) asegurar extensiones útiles (opcional)
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 3) ejecutar scripts en orden (relative include)
\ir 001_enums.sql
\ir 002_users_roles.sql
\ir 003_catalogs.sql
\ir 004_inventory.sql

-- 4) seeds (opcional)
\if :{?LOAD_SEED}
  \echo Loading seeds...
  \ir 999_seed.sql
\endif

\echo Done ✔
