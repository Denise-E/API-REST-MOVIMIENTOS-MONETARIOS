from pydantic import BaseModel

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
    cantCuentas: int #Solo necesito cantidad para crearlas ya que cuenta tiene columns id (autoincremental) y id_cliente
    

    class Config:
        orm_mode = True

class ClienteDetail(BaseModel):
    id: int
    dni: int
    nombre: str 
    categorias: list[object]
    cuentas: list[object]

    class Config:
        orm_mode = True

