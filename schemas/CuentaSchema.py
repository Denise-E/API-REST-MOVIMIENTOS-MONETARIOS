from pydantic import BaseModel

class Cuenta(BaseModel): 
    id: int 
    id_cliente: int

    class Config:
        orm_mode = True


class CuentaSaldo(BaseModel):
    saldo_ARS: float
    saldo_USD: float

    class Config:
        orm_mode = True