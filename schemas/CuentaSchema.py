from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CuentaBase(BaseModel):
    id_cliente: int 

class CuentaCreate(CuentaBase):
    pass


class Cuenta(CuentaBase): 
    id: int 

    class Config:
        orm_mode = True