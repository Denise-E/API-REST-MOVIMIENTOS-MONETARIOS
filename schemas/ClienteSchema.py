from pydantic import BaseModel
from models import Cuenta

class Cliente(BaseModel):
    id: int
    dni: int
    nombre: str 

    class Config:
        orm_mode = True

class ClienteCreate(BaseModel):
    dni: int
    nombre: str 
    categorias: list[int]
    cantCuentas: int #Solo necesito cantidad para crearlas ya que cuenta tiene columns id y id_cliente
    

    class Config:
        orm_mode = True



