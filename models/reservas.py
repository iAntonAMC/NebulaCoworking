
from fastapi.responses import JSONResponse
from fastapi import HTTPException 
from fastapi import status

import os
from supabase import create_client, Client

url: str = "https://eegpspgminmhrajbujkg.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVlZ3BzcGdtaW5taHJhamJ1amtnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzMzNzAwOTgsImV4cCI6MjA0ODk0NjA5OH0.XBDFsIJtYEoHjrjMbjqLSylsxyCBgmYFtkVL0GKemr0"

supabase: Client = create_client(url, key)


# GET ALL
def allReservas():
    try:
        response = supabase.table("reservas").select("*").execute()
        if len(response.data) > 0:
            return JSONResponse(status_code=200, content={"succes": "true", "datos": response.data})
        elif response.data == []:
            return JSONResponse(status_code=400, content={"message": "No se obtuvieron datos de reservas"})
            
    except Exception as error:
        print(f"Error in oficinas.all: {error.args}")
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"Model method dropped an error: {error}"
        )


# CREATE ONE
def createReserva(reserva):
    try:
        
        data = reserva.dict()
        data["fecha_reserva"] = data["fecha_reserva"].strftime("%Y-%m-%d %H:%M:%S")  # Formato para datetime
        data["fecha_inicio"] = data["fecha_inicio"].strftime("%Y-%m-%d")  # Formato para date
        data["fecha_fin"] = data["fecha_fin"].strftime("%Y-%m-%d")  # Formato para date
        print (data)
        response = supabase.table("reservas").insert(data).execute()
        if len(response.data) > 0:
            return JSONResponse(status_code=201, content={"message": "Usuario creado", "data": response.data})
    except Exception as exception:
        return exception

def updateReserva(id_reserva, reserva):
    try:
        data = reserva.dict(exclude_unset=True)
        print (data)
        if "fecha_reserva" in data:
            data["fecha_reserva"] = data["fecha_reserva"].strftime("%Y-%m-%d %H:%M:%S")
        if "fecha_inicio" in data:
            data["fecha_inicio"] = data["fecha_inicio"].strftime("%Y-%m-%d") 
        if "fecha_fin" in data:
            data["fecha_fin"] = data["fecha_fin"].strftime("%Y-%m-%d")
        response = supabase.table("reservas").update(data).eq("id_reserva", id_reserva).execute()
        
        if len(response.data) > 0:
            return JSONResponse(status_code=200, content={"success": True, "data": response.data})
        elif response == []:
            return JSONResponse(status_code=400, content={"success": False, "message": "Error al actualizar los datos"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error en el servidor", "error": str(e)})


def deleteReserva(id_reserva):
    try:
        response = supabase.table("reservas").delete().eq("id_reserva", id_reserva).execute()
        if len(response.data) > 0:
            return JSONResponse(status_code=200, content={"sucess": True, "data": response.data})
        elif response.data == []:
            return JSONResponse(status_code=400, content={"sucess": False, "message": "No se encontro el id de la reserva"})
        
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"succes": False, "message": "Error en el servidor", "error": str(e)})