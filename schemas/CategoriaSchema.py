from pydantic import BaseModel

class CategoriaBase(BaseModel):
    id: int
    nombre: str 

    class Config:
        orm_mode = True

