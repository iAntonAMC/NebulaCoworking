from fastapi import HTTPException
from fastapi.responses import JSONResponse
from supabase import create_client, Client
from supabase.client import ClientOptions
from pydantic import EmailStr
import bcrypt


# SUPABASE CONFIG
url: str = "https://eegpspgminmhrajbujkg.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVlZ3BzcGdtaW5taHJhamJ1amtnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzMzNzAwOTgsImV4cCI6MjA0ODk0NjA5OH0.XBDFsIJtYEoHjrjMbjqLSylsxyCBgmYFtkVL0GKemr0"


# Crear cliente de Supabase
supabase: Client = create_client(url, key, 
    options=ClientOptions(
        postgrest_client_timeout=10,
        storage_client_timeout=10,
        schema="public",
    ))


# FUNCIONES
def encriptar_contraseña(contraseña: str) -> str:
    return bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verificar_contraseña(contraseña_ingresada: str, contraseña_guardada: str) -> bool:
    return bcrypt.checkpw(contraseña_ingresada.encode('utf-8'), contraseña_guardada.encode('utf-8'))


# Función de registro
def registro_usuario(nombre: str, correo: EmailStr, contraseña: str, tipo_usuario: str, id_empresa: int):
    try:
        # Verificar si el correo ya está registrado
        existing_user = supabase.table('usuarios').select('correo').eq('correo', correo).execute().data
        if existing_user:
            return JSONResponse(status_code=400, content={"message": "Correo ya registrado"})

        # Encriptar la contraseña
        contraseña_encriptada = encriptar_contraseña(contraseña)

        # Verificar si el 'id_empresa' es 0 o None
        id_empresa = None if id_empresa in (None, 0) else id_empresa

        # Insertar el nuevo usuario en la base de datos
        response = supabase.table('usuarios').insert({
            "nombre": nombre,
            "correo": correo,
            "contraseña": contraseña_encriptada,
            "tipo_usuario": tipo_usuario,
            "id_empresa": id_empresa  # Inserta 'id_empresa' también
        }).execute()

        if response.data:
            return {"message": "Usuario registrado exitosamente"}
        else:
            return JSONResponse(status_code=500, content={"message": "Error al registrar el usuario"})
    except Exception as error:
        print(f"Error en el registro: {error.args}")
        raise HTTPException(
            status_code=400,
            detail=f"Error al registrar el usuario: {error}"
        )

# Función de login
def login_usuario(correo: str, contraseña: str):
    try:
        # Obtener datos del usuario por correo
        user_data = supabase.table('usuarios').select('id_usuario', 'nombre', 'correo', 'contraseña').eq('correo', correo).execute().data
        
        if not user_data:
            return {"message": "Correo o contraseña incorrectos"}

        user_data = user_data[0]
        
        # Verificar la contraseña ingresada
        if not verificar_contraseña(contraseña, user_data['contraseña']):
            return {"message": "Correo o contraseña incorrectos"}

        return {"message": f"Bienvenido {user_data['nombre']}!", "id_usuario": user_data['id_usuario']}
    except Exception as error:
        print(f"Error en el login: {error.args}")
        raise HTTPException(
            status_code=400,
            detail=f"Error en el login: {error}"
        )