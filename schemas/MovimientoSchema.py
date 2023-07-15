from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MovimientoBase(BaseModel):
    id_cuenta = int # Va aca?
    tipo = int
    importe = float
    fecha = datetime


class MovimientoCreate(MovimientoBase):
    pass

class Movimiento(MovimientoBase):
    id: int
    tipo = int
    importe = float
    fecha = datetime

    class Config:
        orm_mode = True
