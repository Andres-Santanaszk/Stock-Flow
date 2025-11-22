# security/hashing.py
import bcrypt

def hash_password(plain_password: str) -> str:
    """
    Recibe una contraseña en texto plano y retorna su hash con salt usando bcrypt.
    Retorna str para facilitar el almacenamiento en PostgreSQL (VARCHAR/TEXT).
    """
    # bcrypt requiere bytes, así que encodeamos
    password_bytes = plain_password.encode('utf-8')
    
    # Generamos el salt y hasheamos
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    
    # Retornamos como string decodificado
    return hashed_bytes.decode('utf-8')

def check_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña coincide con el hash guardado.
    Útil para tu módulo de Login.
    """
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(password_bytes, hashed_bytes)