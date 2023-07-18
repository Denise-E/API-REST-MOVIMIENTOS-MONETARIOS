from fastapi import HTTPException
import datetime

def validate_client_dni(dni):
    #No valido que sea extactamente de 8 dígitos porque en otro países se que tienen más.
    dni = str(dni)
    if len(dni) < 8: 
        raise HTTPException(status_code=404, detail="Ingrese un dni valido")
    

def validate_client_name(name):
    #Ni un string vacio ni mayor a 200, tamaño definido en la base de datos
    if len(name) <= 0 or len(name) > 200:
        raise HTTPException(status_code=404, detail="Ingrese un nombre valido")


def validate_movement_mount(mount):
    if mount <= 0:
        raise HTTPException(status_code=404, detail="Ingrese un monto valido")
    