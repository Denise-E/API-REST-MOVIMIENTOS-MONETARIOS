from fastapi import APIRouter,HTTPException
from fastapi import Depends
from config.database import SessionLocal
from sqlalchemy.orm import Session
from crud import clientes as crud
from schemas import ClienteSchema as schema

cliente = APIRouter()

# DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Listado de todos sus clientes, sin detalles de sus cuentas ni catgeorias
@cliente.get("/clientes", response_model=list[schema.Cliente])
def read_clients(skip: int = 0, db: Session = Depends(get_db)):
    clientes = crud.get_clientes(db, skip=skip)
    return clientes


'''
Creación de un cliente. Al crearse también se crearán 1 o más cuentas con sus respectivas
categorias. El alta de estos últimos no deben hacerse por consigna pero si estan incluidos
los campos en el esquema.
'''
#Agregar valdiacion de que no exista el cliente.
@cliente.post('/clientes',response_model=schema.Cliente)
def create_client(input: schema.ClienteCreate,db: Session = Depends(get_db)):
    new_client = crud.create_mov(db, input)
    if new_client is None:
        raise HTTPException(status_code=404, detail="No se pudo registrar el cliente")
    return new_client
