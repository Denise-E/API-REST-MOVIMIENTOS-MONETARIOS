from pydantic import BaseModel
from datetime import datetime

class Movimiento(BaseModel):
    id: int
    id_cuenta: int
    tipo: int
    importe: float
    fecha: datetime
    
    class Config:
        orm_mode = True

class MovimientoCreate(BaseModel):
    id_cuenta: int
    tipo: int
    importe: float
    
    class Config:
        orm_mode = True
        
