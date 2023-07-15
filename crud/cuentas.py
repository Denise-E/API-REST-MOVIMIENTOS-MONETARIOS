from sqlalchemy.orm import Session
import models.Cuenta as model


def get_cuentasPorCliente(db: Session,client_id: int):
    return db.query(model.Cuenta).filter(model.Cuenta.id_cliente == client_id).all()