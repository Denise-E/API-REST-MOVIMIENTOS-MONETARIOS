from sqlalchemy.orm import Session
import models.Cliente as model
from schemas import ClienteSchema as schema


def get_clientes(db: Session, skip: int = 0):
    return db.query(model.Cliente).offset(skip).all()

def create_mov(db: Session, data:schema.ClienteCreate):
    #Creacion cliente. Mismo proceso deberia hacerlo con el modelo de las tablas cuentas y categorias
    new_client = model.Cliente(dni = data.dni, nombre = data.nombre)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

