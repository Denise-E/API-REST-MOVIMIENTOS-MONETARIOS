from sqlalchemy.orm import Session

from . import models, schemas


def get_cliente(db: Session, cliente_id: int):
    return db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

def get_clientes(db: Session, skip: int = 0):
    return db.query(models.Cliente).offset(skip).all()

def get_cuentasPorClientes(db: Session, cliente_id: int): 
    return db.query(models.Cuenta).filter(models.Cuenta.id_cliente == cliente_id).all()

def get_movimientoPorCuenta(db: Session, cuenta_id: int):
    return db.query(models.Movimiento).filter(models.Movimiento.id_cuenta == cuenta_id).all()

def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    db_cliente = models.Cliente(nombre=cliente.nombre)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def delete_cliente(db: Session, cliente_id: int): #MODULARIZAR
    cuentas_cliente = get_cuentasPorClientes(db,cliente_id) 
    for i in range(0,len(cuentas_cliente)):
        movimientos_cuenta = get_movimientoPorCuenta(db,cuentas_cliente[i].id)
        for i in range(0,len(movimientos_cuenta)):
            db.delete(cuentas_cliente[i])
            db.commit()
        db.delete(cuentas_cliente[i])
    db.commit()
    cliente = get_cliente(db, cliente_id)
    db.delete(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

def get_movimiento(db: Session, movimiento_id: int):
    return db.query(models.Movimiento).filter(models.Movimiento.id == movimiento_id).first()

def delete_movimiento(db: Session, movimiento_id: int):
    movimiento = get_movimiento(db, movimiento_id)
    db.delete(movimiento)
    db.commit()
    db.refresh(movimiento)
    return movimiento

