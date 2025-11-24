# crear_admin.py
from entities.User import User 
# Ajusta la importación si tu archivo se llama diferente (ej: from models.user import User)

def registrar_admin():
    print("--- Creando Usuario Administrador ---")
    
    # Datos del nuevo usuario
    nombre = "Administrador"
    email = "admin"  # O usa un correo real tipo "admin@stockflow.com"
    password = "1234" # Esta será la contraseña que usarás para entrar
    role_id = 1      # Asumiendo que 1 es el ID para rol de admin
    
    # Creamos el objeto User
    nuevo_usuario = User(
        full_name=nombre,
        email=email,
        password=password,
        role_id=role_id,
        active=True
    )
    
    # Guardamos en BD (esto llamará a tu nuevo método create y hará el hash)
    if nuevo_usuario.create():
        print("¡Éxito! Ahora puedes iniciar sesión en la app.")
    else:
        print("Hubo un error al crear el usuario.")

if __name__ == "__main__":
    registrar_admin()