-- BRANDS
CREATE TABLE IF NOT EXISTS brands (
  id_brand SERIAL PRIMARY KEY,
  name VARCHAR(120) NOT NULL UNIQUE,
  description TEXT,
  website VARCHAR(255),
  contact_email VARCHAR(150),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);