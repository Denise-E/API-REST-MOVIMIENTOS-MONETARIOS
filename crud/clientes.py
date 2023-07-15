from sqlalchemy.orm import Session
import models.Cliente as model
from schemas import ClienteSchema as schema
from crud import categorias as crud_categorias
from crud import cuentas as crud_cuentas

def get_clientes(db: Session, skip: int = 0):
    return db.query(model.Cliente).offset(skip).all()

def get_clientePorId(db: Session,client_id: int):
    return db.query(model.Cliente).filter(model.Cliente.id == client_id).first()

def get_clienteDetail(db: Session,client_id: int):
    client = get_clientePorId(db,client_id)
    clientDetail = None

    if client is not None:
        client_category = crud_categorias.get_categoriasPorCliente(db,client.id)
        client_account = crud_cuentas.get_cuentasPorCliente(db,client.id)
        clientDetail = schema.ClienteDetail(id = client.id, dni = client.dni, nombre =client.nombre, categorias = client_category, cuentas = client_account)
     
    return clientDetail


def create_mov(db: Session, data:schema.ClienteCreate):
    #Creacion cliente. Mismo proceso deberia hacerlo con el modelo de las tablas cuentas y categorias
    new_client = model.Cliente(dni = data.dni, nombre = data.nombre)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

