from sqlalchemy.orm import Session
import models.Categoria_Cliente as model


def get_categoriasPorCliente(db: Session,client_id: int):
    return db.query(model.Categoria_Cliente).filter(model.Categoria_Cliente.id_cliente == client_id).all()