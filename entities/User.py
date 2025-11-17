import psycopg2 
from db.connection import get_connection
from security.hashing import PasswordManager

class User:
    def __init__(self, id_user=None, full_name=None, email=None, password=None, active=True, role_id=None, create_at=None, updated_at=None):
        self.id_user = id_user
        self.full_name = full_name
        self.email = email
        self.password = password
        self.active = active
        self.role_id = role_id
        self.created_at = create_at
        self.updated_at = updated_at
    
    def create(self):
        """
        Inserta un nuevo usuario en la base de datos, generando el hash seguro 
        de su contraseña con bcrypt antes de guardarla.
        """
        # 1. Encriptamos la contraseña plana que tiene el objeto
        if not self.password:
            raise ValueError("La contraseña no puede estar vacía")
            
        hashed_password = PasswordManager.hash_password(self.password)
        
        # 2. Preparamos la consulta SQL
        # Asumo que tu tabla tiene columnas: full_name, email, password, role_id
        # Si tu columna se llama 'password_hash' en la BD, cámbialo abajo
        sql = """
            INSERT INTO users (full_name, email, password_hash, role_id, active)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_user;
        """
        
        conn = get_connection()
        try:
            cur = conn.cursor()
            # Ejecutamos el insert pasando el HASH, no la plana
            cur.execute(sql, (
                self.full_name,
                self.email,
                hashed_password, # ¡IMPORTANTE! Guardamos el hash
                self.role_id,
                self.active
            ))
            
            # Obtenemos el ID generado y confirmamos cambios
            self.id_user = cur.fetchone()[0]
            conn.commit()
            print(f"Usuario creado con ID: {self.id_user}")
            return True
            
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()

    def update(self):
        """
        Actualiza la información del usuario, como su nombre, correo o rol
        """
        pass

    def check_password(self):
        """
        Verifica si la contraseña ingresada coincide con el hash guardado utilizando bcrypt.checkpw()
        """
        pass

    @staticmethod
    def authenticate(email, plain_password):
        """
        Comprueba las credenciales de un usuario, si el correo existe y la contraseña es correcta, devuelve el usuario; de lo contrario, devuelve, None
        """
        """
        1. Busca el usuario por email.
        2. Si existe, obtiene su hash.
        3. Usa PasswordManager para comparar.
        4. Retorna el objeto User si es correcto, None si falla.
        """
        # Asegúrate que el nombre de la columna de la contraseña sea correcto (ej: password o password_hash)
        sql = """
            SELECT id_user, full_name, email, password_hash, active, role_id 
            FROM users 
            WHERE email = %s AND active = true 
            LIMIT 1;
        """
        
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(sql, (email,))
            row = cur.fetchone()
            
            if row:
                # Desempaquetamos los datos de la BD
                # Asumiendo orden: id, nombre, email, hash, active, role
                db_id, db_name, db_email, db_hash, db_active, db_role = row
                
                # VERIFICACIÓN DE CONTRASEÑA
                if PasswordManager.check_password(plain_password, db_hash):
                    # Creamos y retornamos el objeto usuario
                    return User(id_user=db_id, full_name=db_name, email=db_email, role_id=db_role)
            
            return None # Usuario no encontrado o contraseña incorrecta
            
        except Exception as e:
            print(f"Error en autenticación: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def list_all():
        """
        Obtiene una lista de todos los usuarios registrados, con opción de filtrar por estado activo.
        """
        pass

    def __repr__(self):
        """
        Devuelve una representación corta del usuario mostrando su nombre y correo
        """
        pass