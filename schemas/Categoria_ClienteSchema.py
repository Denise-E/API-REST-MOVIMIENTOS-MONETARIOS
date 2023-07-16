from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Categoria_ClienteBase(BaseModel):
    id_categoria: int
    id_cliente: int

    class Config:
            orm_mode = True

class Categoria_ClienteCreate(BaseModel):
    id_categoria: int

    class Config:
            orm_mode = True

