from datetime import datetime
from typing import List
from pydantic import BaseModel
from pydantic import EmailStr
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
# Model Imports
from models.chats import ChatByID, create_chat, create_message

app = FastAPI()

class Chat(BaseModel):
    id_chat: int
    nombre_chat: str
    fecha_creacion: str

class ChatCreate(BaseModel):
    nombre_chat: str

class MessageCreate(BaseModel):
    id_chat: int
    id_emisor: int
    contenido: str

@app.get("/")
async def read_root():
    return {"message": "API Arriba"}

# Check Connection
@app.get("/connect")
async def connect_to_supabase():
    try:
        response = supabase.table('usuarios').select('*').execute()
        if response.data:
            return {"message": "Conexión exitosa con Supabase"}
        else:
            return {"message": "No se encontraron datos en la tabla 'usuarios'"}
    except Exception as e:
        return {"message": f"Error en la conexión: {str(e)}"}

# Get Chat by ID
@app.get("/chats/{id_chat}", response_model=Chat, status_code=status.HTTP_200_OK)
async def getChatByID(id_chat: int):
    try:
        response = ChatByID(id_chat)
        if isinstance(response, JSONResponse):
            return response
        return response
    except Exception as error:
        print(f"ERROR en getChatByID: {error.args}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": f"Error: {error}"}
        )

# Create Chat
@app.post("/chats/", response_model=ChatCreate, status_code=status.HTTP_201_CREATED)
async def create_chat_endpoint(chat: ChatCreate):
    try:
        created_chat = create_chat(chat.nombre_chat)
        if created_chat:
            return ChatCreate(
                nombre_chat=created_chat['nombre_chat'],
            )
        else:
            raise HTTPException(status_code=400, detail="Error al crear el chat")
    except Exception as error:
        print(f"Error en create_chat_endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en la creación del chat: {error}"
        )

# Create Message
@app.post("/mensajes/", status_code=status.HTTP_201_CREATED)
async def create_message_endpoint(message: MessageCreate):
    try:
        created_message = create_message(message.id_chat, message.id_emisor, message.contenido)

        if created_message:
            return {
                "id_chat": created_message['id_chat'],
                "id_emisor": created_message['id_emisor'],
                "contenido": created_message['contenido'],
                "fecha_envio": created_message['fecha_envio'],
            }
        else:
            raise HTTPException(status_code=400, detail="Error al crear el mensaje")
    
    except Exception as error:
        print(f"Error en create_message_endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en la creación del mensaje: {error}"
        )

# Get Messages by Chat ID
