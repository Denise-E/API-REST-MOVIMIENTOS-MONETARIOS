from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Tipo_MovimientoBase(BaseModel):
    tipo: str 


class Tipo_MovimientoCreate(Tipo_MovimientoBase):
    pass


class Tipo_Movimiento(Tipo_MovimientoBase): 
    id: int 

    class Config:
        orm_mode = True