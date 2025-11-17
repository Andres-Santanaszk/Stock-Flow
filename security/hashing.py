import bcrypt

class PasswordManager:
    """
    Una clase de utilidad para manejar la encriptación y verificación
    de contraseñas usando bcrypt.
    
    Usamos métodos estáticos (@staticmethod) porque no necesitamos
    almacenar ningún estado (no usamos 'self').
    """
    
    @staticmethod
    def hash_password(plain_password: str) -> str:
        """
        Genera un hash de una contraseña de texto plano.
        
        Args:
            plain_password: La contraseña en texto plano (ej: "1234").
        
        Returns:
            El hash de la contraseña como un string (ej: "$2b$12$...").
        """
        # Codifica la contraseña a bytes, que es lo que bcrypt espera
        password_bytes = plain_password.encode('utf-8')
        
        # Genera un "salt" (un valor aleatorio)
        salt = bcrypt.gensalt()
        
        # Genera el hash
        hashed_bytes = bcrypt.hashpw(password_bytes, salt)
        
        # Decodifica de nuevo a string para poder almacenarlo fácilmente
        # en una base de datos o un diccionario.
        return hashed_bytes.decode('utf-8')

    @staticmethod
    def check_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifica si una contraseña de texto plano coincide con un hash.
        
        Args:
            plain_password: La contraseña que el usuario introduce (ej: "1234").
            hashed_password: El hash que tienes almacenado en tu BD (ej: "$2b$12$...").
            
        Returns:
            True si la contraseña es correcta, False si no lo es.
        """
        try:
            # Codifica ambas contraseñas a bytes
            plain_bytes = plain_password.encode('utf-8')
            hashed_bytes = hashed_password.encode('utf-8')
            
            # bcrypt.checkpw hace la comparación de forma segura
            # y tarda un tiempo constante para prevenir "timing attacks".
            return bcrypt.checkpw(plain_bytes, hashed_bytes)
        except ValueError:
            # Esto puede pasar si el hash almacenado no es válido
            return False