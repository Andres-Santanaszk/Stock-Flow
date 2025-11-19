from db.connection import get_connection

class User:
    def __init__(
        self,
        full_name,
        email,
        password_hash,
        active=True,
        role_id=None,
        id_user=None,
    ):
        self.id_user = id_user
        self.full_name = full_name
        self.email = email
        self.password_hash = password_hash # password_hash YA VENDRA HASHEADO
        self.active = active
        self.role_id = role_id

    def add_user(self):
        """
        Inserta un nuevo usuario en la tabla users.
        Si ya tiene id_user, en lugar de insertar llama a update().
        """
        if self.id_user is not None:
            return self.update()

        sql = """
        INSERT INTO users
            (full_name, email, password_hash, role_id)
        VALUES
            (%s, %s, %s, %s)
        RETURNING id_user;
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                sql,
                (
                    self.full_name,
                    self.email,
                    self.password_hash,
                    self.role_id,
                ),
            )
            row = cur.fetchone()
            conn.commit()

            self.id_user = row[0]
            return self.id_user
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    def update(self):
        """
        Actualiza los datos del usuario existente.
        """
        if self.id_user is None:
            raise ValueError("No puedes actualizar un usuario sin id_user. Guárdalo primero.")

        sql = """
        UPDATE users
           SET full_name     = %s,
               email         = %s,
               password_hash = %s,
               active        = %s,
               role_id       = %s
         WHERE id_user = %s;
        """
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                sql,
                (
                    self.full_name,
                    self.email,
                    self.password_hash,
                    self.active,
                    self.role_id,
                    self.id_user,
                ),
            )
            if cur.rowcount == 0:
                raise ValueError(f"No existe users.id_user = {self.id_user}")

            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    def __repr__(self):
        return f"<User id={self.id_user} email={self.email} role_id={self.role_id}>"
