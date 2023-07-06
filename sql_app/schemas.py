from pydantic import BaseModel
from datetime import datetime

class ClienteBase(BaseModel):
    nombre: str 
    #Al crearlo no sabemos id ya que se deifne al crearse el registro en la BBDD


class ClienteCreate(ClienteBase):
    pass


class Cliente(ClienteBase): #Lo que obtendremos de la API
    id: int 

    class Config:
        orm_mode = True

class CuentaBase(BaseModel):
    id_cliente: int 

class CuentaCreate(CuentaBase):
    pass


class Cuenta(CuentaBase): 
    id: int 

    class Config:
        orm_mode = True

class MovimientoBase(BaseModel):
    id_cuenta = int # Va aca?
    tipo = int
    importe = float
    fecha = datetime

class MovimientoCreate(MovimientoBase):
    pass


class Movimiento(MovimientoBase): 
    id: int 

    class Config:
        orm_mode = True


class Tipo_MovimientoBase(BaseModel):
    tipo: str 


class Tipo_MovimientoCreate(Tipo_MovimientoBase):
    pass


class Tipo_Movimiento(Tipo_MovimientoBase): 
    id: int 

    class Config:
        orm_mode = True

class CategoriaBase(BaseModel):
    nombre: str 

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase): 
    id: int 

    class Config:
        orm_mode = True

'''class Categoria_ClienteBase(BaseModel):
    id_categoria = int
    id_cliente = int

class Categoria_ClienteCreate(Categoria_ClienteBase):
    pass

class Categoria_Cliente(Categoria_ClienteBase): 
    pass

    class Config:
        orm_mode = True'''