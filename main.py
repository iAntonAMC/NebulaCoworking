from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from pydantic import EmailStr
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime, date
# Model Imports
from models.chats import ChatByID, create_chat, create_message, get_messages_by_chat_id
from models.register import registro_usuario, login_usuario
import models.reservas as reservas
import models.oficina as oficinas



app = FastAPI()

# Modelo CRUD para oficina

class Oficina(BaseModel):
    id_propietario: Optional[int] = None 
    nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    descripcion: Optional[str] = None
    capacidad_maxima: Optional[int] = None
    precio: Optional[float] = None
    disponibilidad: Optional[bool] = None
    fecha_creacion: Optional[datetime] = None

# Modelo CRUD para reserva

class Reserva(BaseModel):
    id_oficina: Optional[int] = None
    id_coworker: Optional[int] = None
    numero_colaboradores: Optional[int] = None
    monto_total: Optional[float] = None
    fecha_reserva: Optional[datetime] = None  
    fecha_inicio: Optional[date] = None       
    fecha_fin: Optional[date] = None     

### MODELOS BASE MODEL PARA USUARIOS ###

class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    tipo_usuario: str  # propietario o coworker

class UsuarioRegistro(BaseModel):
    nombre: str
    correo: EmailStr
    contraseña: str
    tipo_usuario: str  # Este campo debe existir
    id_empresa: int  # Asegúrate de que 'id_empresa' esté definido

class UsuarioLogin(BaseModel):
    correo: EmailStr
    contraseña: str

### MODELOS BASE MODEL PARA CHATS ###

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

class Message(BaseModel):
    id_mensaje: int
    id_chat: int
    id_emisor: int
    contenido: str
    fecha_envio: str

class MessagesResponse(BaseModel):
    messages: List[Message]

@app.get("/")
async def read_root():
    return {"message": "API Arriba"}

### MODELOS PARA LOGIN Y REGISTRO ###

@app.post("/registro", status_code=status.HTTP_201_CREATED)
async def registro(usuario: UsuarioRegistro):
    try:
        # Aquí llamamos a la función sin 'await' ya que no es asincrónica
        response = registro_usuario(usuario.nombre, usuario.correo, usuario.contraseña, usuario.tipo_usuario, usuario.id_empresa)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error en el registro: {str(e)}")


@app.post("/login", status_code=status.HTTP_200_OK)
async def login(usuario: UsuarioLogin):
    try:
        # Usamos la función de login directamente sin pasar supabase como argumento
        response = login_usuario(usuario.correo, usuario.contraseña)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error en el login: {str(e)}")

#### MODELOS PARA EL CHAT#####

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
@app.get("/mensajes/{id_chat}", status_code=status.HTTP_200_OK)
async def get_messages_endpoint(id_chat: int):
    try:
        # Llamamos a la función para obtener los mensajes del chat
        messages_data = get_messages_by_chat_id(id_chat)

        if messages_data:
            # Mapeamos los mensajes a la estructura de la respuesta del modelo
            messages = [Message(
                id_mensaje=msg['id_mensaje'],
                id_chat=msg['id_chat'],
                id_emisor=msg['id_emisor'],
                contenido=msg['contenido'],
                fecha_envio=msg['fecha_envio']
            ) for msg in messages_data]

            return MessagesResponse(messages=messages)
        else:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No se encontraron mensajes para este chat"})

    except Exception as error:
        print(f"Error en get_messages_endpoint: {error}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al obtener los mensajes: {error}"
        )
