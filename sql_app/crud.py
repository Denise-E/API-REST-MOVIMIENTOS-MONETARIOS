from sqlalchemy.orm import Session

from . import models, schemas


def get_cliente(db: Session, client_id: int):
    return db.query(models.Cliente).filter(models.Cliente.id == client_id).first()

def get_clientes(db: Session, skip: int = 0):
    return db.query(models.Cliente).offset(skip).all()

def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    db_cliente = models.User(nombre=cliente.nombre)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def get_movimiento(db: Session, movimiento_id: int):
    return db.query(models.Movimiento).filter(models.Movimiento.id == movimiento_id).first()
