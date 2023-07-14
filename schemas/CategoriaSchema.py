from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CategoriaBase(BaseModel):
    nombre: str 

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase): 
    id: int 

    class Config:
        orm_mode = True
