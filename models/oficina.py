import sqlite3
from fastapi.responses import JSONResponse
from fastapi import HTTPException 
from fastapi import status
from supabase import create_client, Client

url: str = "https://eegpspgminmhrajbujkg.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVlZ3BzcGdtaW5taHJhamJ1amtnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzMzNzAwOTgsImV4cCI6MjA0ODk0NjA5OH0.XBDFsIJtYEoHjrjMbjqLSylsxyCBgmYFtkVL0GKemr0"


supabase: Client = create_client(url, key)


# GET ALL
def allOficinas():
    try:
        response = supabase.table("oficinas").select("*").execute()
        if len(response.data) > 0:
            return JSONResponse(status_code=200, content={"succes": "true", "datos": response.data})
        elif response.data == []: 
            return JSONResponse(status_code=400, content={"message": "No se obtuvieron datos de oficinas"})
    except Exception as error:
        print(f"Error in oficinas.all: {error.args}")
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"Model method dropped an error: {error}"
        )
    

def insertOficina(oficina):
    try:
        data = oficina.dict()
        response = supabase.table("oficinas").insert(data).execute()
        
        if len(response.data) > 0:
            return response
    except Exception as exception:
        
        if isinstance(exception, dict) and "code" in exception:
            
            print("Error al insertar los datos:", exception)
            return JSONResponse(
                status_code=400,
                content={
                    "message": "Error al insertar la oficina",
                    "error": exception.get("message"),
                    "details": exception.get("details"),
                    "code": exception.get("code"),
                },
            )
        
        print("Excepción al insertar la oficina:", str(exception))
        return JSONResponse(
            status_code=500,
            content={"message": "Error interno del servidor", "error": str(exception)},
        )
def updateOficina(id_oficina, oficina):
    try:
        print(id_oficina)
        data = oficina.dict(exclude_unset = True)
        print(data)
        if "fecha_creacion" in data:
            data["fecha_creacion"] = data["fecha_creacion"].strftime("%Y-%m-%d %H:%M:%S")
        response = supabase.table("oficinas").update(data).eq("id_oficina", id_oficina).execute()
        print (response)
        if len(response.data) > 0:
            return JSONResponse(status_code=200, content={"succes": "true", "data": response.data})
        else:
            return response
    except Exception as e:
        print(f"Error general: {str(e)}")
        return JSONResponse(status_code=500, content={"success": False, "message": "Error en el servidor", "error": str(e)})
    
def deleteOficina(id_oficina):
    try:
        response = supabase.table("oficinas").delete().eq("id_oficina", id_oficina).execute()
        if len(response.data) > 0:
            return JSONResponse(status_code=200, content={"sucess": True, "data": response.data})
        elif response.data == []:
            return JSONResponse(status_code=400, content={"sucess": False, "message": "No se encontro el id de la oficina"})
        
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"succes": False, "message": "Error en el servidor", "error": str(e)})