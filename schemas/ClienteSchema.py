from pydantic import BaseModel
from typing import Optional

class ClienteBase(BaseModel): #Los datos que nos van a llegar.
    id: Optional[int]
    dni: int
    nombre: str 


class ClienteCreate(ClienteBase):
    pass


class Cliente(ClienteBase):
    id: int 

    class Config:
        orm_mode = True