from db.connection import get_connection
from security.hashing import check_password

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
        self.password_hash = password_hash
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
            count = cur.fetchone()[0]
            
            return count > 0
            
        except Exception as e:
            print(f"Error checking email: {e}") 
            raise e
        finally:
            if cur: cur.close()
            if conn: conn.close()

    @staticmethod
    def get_users():
        """
        Retorna usuarios haciendo JOIN con roles para obtener el nombre.
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
        sql = """
        SELECT 
            u.id_user, 
            u.full_name, 
            u.email, 
            r.name as role_name,
            u.active
        FROM users u
        LEFT JOIN roles r ON u.role_id = r.id
        WHERE (%s = '' OR LOWER(u.full_name) LIKE LOWER(%s))
        ORDER BY u.id_user ASC;
        """
        
        search_term = name_fragment if name_fragment else ""
        pattern = f"%{search_term}%"
        
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (search_term, pattern))
            rows = cur.fetchall()
            return rows
        except Exception as e:
            print(f"Error searching users: {e}")
            return []
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def get_by_id(user_id):
        """Recupera un usuario por su ID para llenado de formularios."""
        sql = "SELECT id_user, full_name, email, password_hash, active, role_id FROM users WHERE id_user = %s"
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (user_id,))
            row = cur.fetchone()
            if row:
                return User(
                    id_user=row[0],
                    full_name=row[1],
                    email=row[2],
                    password_hash=row[3],
                    active=row[4],
                    role_id=row[5]
                )
            return None
        finally:
            cur.close()
            conn.close()        
            
    @staticmethod
    def search_users_with_role(search_query=""):
        """
        Realiza un JOIN para obtener el nombre del rol en lugar del ID.
        Retorna: (id_user, full_name, email, role_name, active)
        """
        
        sql = """
        SELECT 
            u.id_user, 
            u.full_name, 
            u.email, 
            COALESCE(r.name, 'Sin Rol') as role_name, 
            u.active
        FROM users u
        LEFT JOIN roles r ON u.role_id = r.id
        WHERE (%s = '' OR LOWER(u.full_name) LIKE LOWER(%s))
        ORDER BY u.id_user ASC;
        """
        

        term = search_query if search_query else ""
        pattern = f"%{term}%"

        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (term, pattern))
            rows = cur.fetchall()
            return rows
        except Exception as e:
            print(f"Error fetching users with roles: {e}")
            return []
        finally:
            if cur: cur.close()
            if conn: conn.close()
    
    @staticmethod
    def authenticate(email, password_plain):
        """
        Verifica credenciales.
        Retorna el objeto User si es válido, o None si falla.
        """
        sql = """
        SELECT id_user, full_name, email, password_hash, active, role_id 
        FROM users 
        WHERE email = %s;
        """
        
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (email,))
            row = cur.fetchone()
            
            if not row:
                return None

            id_user, name, db_email, db_hash, active, role_id = row

            if not active:
                print("Intento de login de usuario inactivo.")
                return None 

            if check_password(password_plain, db_hash):
                return User(
                    id_user=id_user,
                    full_name=name,
                    email=db_email,
                    password_hash=db_hash, 
                    active=active,
                    role_id=role_id
                )
            else:
                return None

        except Exception as e:
            print(f"Error de autenticación: {e}")
            return None
        finally:
            cur.close()
            conn.close()        
    
    def __repr__(self):
        return f"<User id={self.id_user} email={self.email} role_id={self.role_id}>"
