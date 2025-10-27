
CREATE TABLE IF NOT EXISTS roles (
  id            SERIAL PRIMARY KEY,
  name          VARCHAR(60)  NOT NULL UNIQUE,   -- p.ej. "Administrador", "Líder"
  description   TEXT
);

CREATE TABLE IF NOT EXISTS permissions (
  id            SERIAL PRIMARY KEY,
  code          VARCHAR(64) NOT NULL UNIQUE,    -- p.ej. "item_view", "movement_register"
  description   TEXT
);

CREATE TABLE IF NOT EXISTS role_permissions (
  role_id        INT NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
  permission_id  INT NOT NULL REFERENCES permissions(id) ON DELETE CASCADE,
  PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE IF NOT EXISTS users (
  id_user        SERIAL PRIMARY KEY,
  full_name      VARCHAR(120)      NOT NULL,     -- nombre completo
  email          VARCHAR(254)      NOT NULL UNIQUE, -- RFC 5321 sugiere 254 máx
  password_hash  VARCHAR(255)      NOT NULL,     -- bcrypt
  active         BOOLEAN           NOT NULL DEFAULT TRUE,
  role_id        INT               REFERENCES roles(id)  -- un usuario = un rol
);
