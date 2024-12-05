from fastapi import HTTPException
from fastapi.responses import JSONResponse
from supabase import create_client, Client
from supabase.client import ClientOptions
from typing import List


# SUPABASE CONFIG
url: str = "https://eegpspgminmhrajbujkg.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVlZ3BzcGdtaW5taHJhamJ1amtnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzMzNzAwOTgsImV4cCI6MjA0ODk0NjA5OH0.XBDFsIJtYEoHjrjMbjqLSylsxyCBgmYFtkVL0GKemr0"

supabase: Client = create_client(url, key, 
    options=ClientOptions(
        postgrest_client_timeout=10,
        storage_client_timeout=10,
        schema="public",
    ))

# FUNCTIONS
def ChatByID(id_chat: int):
    try:
        # Realizar consulta
        response = supabase.table('chats').select('*').eq("id_chat", id_chat).limit(1).execute()
        
        # Verificar si hay datos
        if response.data:
            chat_data = response.data[0]
            chat = {
                "id_chat": chat_data['id_chat'],
                "nombre_chat": chat_data['nombre_chat'],
                "fecha_creacion": chat_data['fecha_creacion'],
            }
            return chat
        else:
            return JSONResponse(status_code=404, content={"message": "Chat no encontrado"})
    except Exception as error:
        print(f"Error en ChatByID: {error.args}")
        raise HTTPException(
            status_code=400,
            detail=f"Error en la consulta del chat: {error}"
        )

def create_chat(nombre_chat: str):
    try:
        response = supabase.table('chats').insert({
            "nombre_chat": nombre_chat,
        }).execute()

        if response.data:
            created_chat = response.data[0] 
            return created_chat
        else:
            return None
    except Exception as error:
        print(f"Error al crear el chat: {error.args}")
        raise Exception(f"Error en la creación del chat: {error}")

def create_message(id_chat: int, id_emisor: int, contenido: str):
    try:
        response = supabase.table('mensajes').insert({
            "id_chat": id_chat,
            "id_emisor": id_emisor,
            "contenido": contenido,
        }).execute()

        if response.data:
            created_message = response.data[0] 
            return created_message
        else:
            return None
    except Exception as error:
        print(f"Error al crear el mensaje: {error.args}")
        raise Exception(f"Error en la creación del mensaje: {error}")

# GET chat messages by chat id
def get_messages_by_chat_id(id_chat: int) -> List[dict]:
    try:
        response = supabase.table('mensajes').select('*').eq("id_chat", id_chat).execute()
        
        if response.data:
            return response.data
        else:
            return []
    except Exception as error:
        print(f"Error al obtener los mensajes: {error.args}")
        raise Exception(f"Error en la obtención de los mensajes: {error}")
