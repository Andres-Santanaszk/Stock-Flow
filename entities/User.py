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

    @staticmethod
    def exists_email(email):
        """
        Verifica si un email ya existe en la base de datos.
        Retorna True si existe, False si no.
        """
        sql = "SELECT COUNT(*) FROM users WHERE email = %s;"
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (email,))
            
            # Fetchone devuelve una tupla, ej: (1,) o (0,)
            count = cur.fetchone()[0]
            
            return count > 0
            
        except Exception as e:
            # Es buena práctica loggear el error, pero aquí lo propagamos
            print(f"Error checking email: {e}") 
            raise e
        finally:
            if cur: cur.close()
            if conn: conn.close()

    @staticmethod
    def get_active_users():
        """
        Retorna usuarios activos haciendo JOIN con roles para obtener el nombre.
        Columns: id_user, full_name, email, role_name
        """
        sql = """
        SELECT 
            u.id_user, 
            u.full_name, 
            u.email, 
            r.name as role_name
        FROM users u
        LEFT JOIN roles r ON u.role_id = r.id
        WHERE u.active = true 
        ORDER BY u.id_user ASC;
        """
        
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            return rows
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []
        finally:
            cur.close()
            conn.close()
            
    @staticmethod
    def search_by_name(name_fragment):
        """
        Busca usuarios activos cuyo nombre coincida parcialmente con el fragmento.
        Retorna: Lista de tuplas (id_user, full_name, email, role_name)
        """
        sql = """
        SELECT 
            u.id_user, 
            u.full_name, 
            u.email, 
            r.name as role_name
        FROM users u
        LEFT JOIN roles r ON u.role_id = r.id
        WHERE u.active = true
          AND (%s = '' OR LOWER(u.full_name) LIKE LOWER(%s))
        ORDER BY u.id_user ASC;
        """
        
        # Si name_fragment es None, usamos cadena vacía para evitar errores
        search_term = name_fragment if name_fragment else ""
        pattern = f"%{search_term}%"
        
        conn = get_connection()
        try:
            cur = conn.cursor()
            # Pasamos search_term para la primera comprobación (%s = '')
            # Y pattern para el LIKE (%s)
            cur.execute(sql, (search_term, pattern))
            rows = cur.fetchall()
            return rows
        except Exception as e:
            print(f"Error searching users: {e}")
            return []
        finally:
            cur.close()
            conn.close()

    def __repr__(self):
        return f"<User id={self.id_user} email={self.email} role_id={self.role_id}>"
