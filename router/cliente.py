from fastapi import APIRouter,HTTPException
from fastapi import Depends
from config.database import SessionLocal
from sqlalchemy.orm import Session

from crud import clientes as crud
from crud import cuentas as crud_accounts
from schemas import ClienteSchema as schema
from schemas import Categoria_ClienteSchema as schema_clientCategory
from schemas import CuentaSchema as schema_accounts

cliente = APIRouter()

# DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Listado de todos sus clientes, sin detalles de sus cuentas ni categorias
@cliente.get("/clientes", response_model=list[schema.Cliente])
def read_clients(skip: int = 0, db: Session = Depends(get_db)):
    clientes = crud.get_clients(db, skip=skip)
    return clientes

#Detalle de cliente con id pasado por URL. Con sus cuentas y categorias.
@cliente.get("/clientes/{client_id}", response_model=schema.ClienteDetail)
def read_clients(client_id: int, db: Session = Depends(get_db)):
    cliente = crud.get_clientDetail(db, client_id = client_id)

    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no existente")
    
    return cliente


'''
Creación de un cliente. Al crearse también se crearán 1 o más cuentas con sus respectivas
categorias. El alta de estos últimos no deben hacerse por consigna pero si estan incluidos
los campos en el esquema.
Valido que no exista previamente el cliente por dni desde crud.create_mov
'''
@cliente.post('/clientes',response_model=schema.Cliente)
def create_client(input: schema.ClienteCreate,db: Session = Depends(get_db)):
    new_client = crud.create_client(db, input)

    if new_client is None:
        raise HTTPException(status_code=404, detail="No se pudo registrar el cliente")
    
    return new_client


#Editar un cliente. En este metodo no se modificaran sus cuentas ni sus categorias, dada la consigna.
@cliente.put("/clientes/{client_id}",response_model=schema.Cliente)
def update_client(client_id: int, input:schema.ClienteUpdate,db: Session = Depends(get_db)):
    client = crud.update_client(client_id, input, db)

    if client is None:
        raise HTTPException(status_code=404, detail="No se pudo actualizar los datos del cliente")
    
    return client


#Eliminacion de un cliente, incluyendo las cuentas y categorias_cliente.
@cliente.delete("/clientes/{client_id}",response_model=schema.Cliente)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = crud.delete_client(db, client_id=client_id)

    if db_client is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return db_client

#Agrega un cliente ya existente a una nueva categoria.
@cliente.post('/clientes/categorias/{client_id}')
def add_clientToCategory(input: schema_clientCategory.Categoria_ClienteCreate,client_id: int, db: Session = Depends(get_db)):
    client = crud.add_clientToCategory(input,db,client_id=client_id)

    if client is None:
        raise HTTPException(status_code=404, detail="No se pudo registrar el cliente a la categoria")
    
    return "Cliente agregado exitosamente a la nueva categoria"


#Detalle de cliente con id pasado por URL. Con sus cuentas y categorias.
@cliente.get("/clientes/cuentas/{account_id}",response_model=schema_accounts.CuentaSaldo)
def read_clients(account_id: int, db: Session = Depends(get_db)):
    cuenta = crud_accounts.get_clientBalance(db, account_id = account_id)

    if cuenta is None:
        raise HTTPException(status_code=404, detail="Cuenta no existente")
    
    return cuenta