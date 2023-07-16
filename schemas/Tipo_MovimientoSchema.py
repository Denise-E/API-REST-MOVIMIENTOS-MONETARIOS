from pydantic import BaseModel


class Tipo_MovimientoBase(BaseModel):
    id: int
    tipo: str 

    class Config:
        orm_mode = True
