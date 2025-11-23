CREATE TABLE IF NOT EXISTS brands (
  id_brand SERIAL PRIMARY KEY,
  name VARCHAR(60) NOT NULL UNIQUE,
  description TEXT,
  website VARCHAR(255),
  contact_email VARCHAR(150) NOT NULL UNIQUE,
  active        BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT chk_brands_contact_email_format
    CHECK (contact_email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE TABLE IF NOT EXISTS categories (
  id_category  SERIAL PRIMARY KEY,
  name         VARCHAR(100) NOT NULL UNIQUE,   
  class        item_class   NOT NULL,          
  description  TEXT,
  active       BOOLEAN      NOT NULL DEFAULT TRUE,
  created_at   TIMESTAMPTZ  NOT NULL DEFAULT now(),
  updated_at   TIMESTAMPTZ  NOT NULL DEFAULT now()
);