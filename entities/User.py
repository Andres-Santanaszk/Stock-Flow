import psycopg2 
from bcrypt import checkpw # Para encriptar

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
        Inserta un nuevo usuario en la base de datos, generando el hash seguro de su contraseña con bcrypt antes de guardarla
        """
        pass

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
    def authenticate():
        """
        Comprueba las credenciales de un usuario, si el correo existe y la contraseña es correcta, devuelve el usuario; de lo contrario, devuelve, None
        """
        pass
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