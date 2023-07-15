from fastapi import HTTPException
from sqlalchemy.orm import Session
import models.Cliente as model
from schemas import ClienteSchema as schema
from crud import categorias as crud_categorias
from crud import cuentas as crud_cuentas

def get_clientes(db: Session, skip: int = 0):
    return db.query(model.Cliente).offset(skip).all()

def get_clientePorId(db: Session,client_id: int):
    return db.query(model.Cliente).filter(model.Cliente.id == client_id).first()

def get_clientePorDni(db: Session,client_dni: int):
    return db.query(model.Cliente).filter(model.Cliente.dni == client_dni).first()

def get_clienteDetail(db: Session,client_id: int):
    client = get_clientePorId(db,client_id)
    clientDetail = None

    if client is not None:
        client_category = crud_categorias.get_categoriasPorCliente(db,client.id)
        client_account = crud_cuentas.get_cuentasPorCliente(db,client.id)
        clientDetail = schema.ClienteDetail(id = client.id, dni = client.dni, nombre =client.nombre, categorias = client_category, cuentas = client_account)
     
    return clientDetail


def create_mov(db: Session, data:schema.ClienteCreate):
    client = get_clientePorDni(db, data.dni) #Valido que no exista ya el cliente por DNI
    new_client = None

    if client is None:
        #Creacion cliente. Mismo proceso deberia hacerlo con el modelo de las tablas cuentas y categorias
        new_client = model.Cliente(dni = data.dni, nombre = data.nombre)
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
    else:
         raise HTTPException(status_code=404, detail="Ya existe un cliente registrado con el DNI ingresado")

    return new_client


def delete_client(db: Session, client_id: int):
    
    client = get_clientePorId(db, client_id=client_id)

    if client is not None:
        client_category = crud_categorias.delete_clientCategories(db,client.id)
        client_account = crud_cuentas.delete_clienteAccounts(db,client.id)
        db.delete(client)
        db.commit()

    return client