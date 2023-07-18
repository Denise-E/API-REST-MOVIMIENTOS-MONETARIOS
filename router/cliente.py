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


#Devuelve el listado de todos los clientes, sin detalles de sus cuentas ni categorias
@cliente.get("/clientes", response_model=list[schema.Cliente], status_code=200)
def read_clients(skip: int = 0, db: Session = Depends(get_db)):
    return crud.get_clients(db, skip=skip)
     

#Muestra el detalle del cliente con el id pasado por URL. Con sus cuentas y categorias.
@cliente.get("/clientes/{client_id}", response_model=schema.ClienteDetail, status_code=200)
def read_client(client_id: int, db: Session = Depends(get_db)):
    #Busca al cliente junto a sus cuentas y categorias. Devuelve un objeto ClienteDetail o None
    cliente = crud.get_clientDetail(db, client_id = client_id) 

    if cliente is None: #Si no se encontró al cliente lanzo excepción con status 404
        raise HTTPException(status_code=404, detail="Cliente no existente")
    
    return cliente #Si se encontró al cliente lo retorno para que sea mostrado en el navegador


'''
Creación de un cliente. Al crearse también se deberían crear una o más cuentas y asociar al cliente con al menos
una categoria. El alta de estos últimos no deben hacerse por consigna pero si estan incluidos los campos en el 
esquema.
'''
@cliente.post('/clientes',response_model=schema.Cliente, status_code=201)
def create_client(input: schema.ClienteCreate,db: Session = Depends(get_db)):
    '''
    Se intenta crear un cliente, realizando las validaciones previas pertinentes desde la carpeta crud.
    Si se pudo crear crud.create_client devolverá un objeto de la clase Cliente, sino None.
    '''
    new_client = crud.create_client(db, input)

    if new_client is None: #Si no se lo pudo registrar lanzo una excepción
        raise HTTPException(status_code=400, detail="No se pudo registrar el cliente")
    
    return new_client #Si se registró al cliente lo devuelvo


#Editar un cliente. En este metodo no se modificaran sus cuentas ni sus categorias, dada la consigna
@cliente.put("/clientes/{client_id}",response_model=schema.Cliente, status_code=200)
def update_client(client_id: int, input:schema.ClienteUpdate,db: Session = Depends(get_db)):
    client = crud.update_client(client_id, input, db) #Actualización del cliente

    if client is None: #Si no pudo actualizarse lanzo excepción informandolo
        raise HTTPException(status_code=400, detail="No se pudo actualizar los datos del cliente")
    
    return client #Si se actualizó muestro los valores actualizados


#Eliminacion de un cliente, incluyendo las cuentas y categorias_cliente
@cliente.delete("/clientes/{client_id}",response_model=schema.Cliente, status_code=200)
def delete_client(client_id: int, db: Session = Depends(get_db)): #Eliminación del cliente
    db_client = crud.delete_client(db, client_id=client_id)

    if db_client is None: 
        #Si no se lanzó una excepción en la ejecución de delete_cliente y el objeto llega vacío informo la situación
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return db_client #Si se eliminó el cliente muestro sus datos 

#Agrega un cliente ya existente a una nueva categoria
@cliente.post('/clientes/categorias/{client_id}',response_model=schema_clientCategory.Categoria_ClienteBase ,status_code=201)
def add_clientToCategory(input: schema_clientCategory.Categoria_ClienteCreate,client_id: int, db: Session = Depends(get_db)):
    #Agrego el cliente a la categoria solicitada realizando las validaciones pertinentes desde el método
    client = crud.add_clientToCategory(input,db,client_id=client_id) 

    if client is None: # Si llegó None informo la situación
        raise HTTPException(status_code=400, detail="No se pudo registrar el cliente a la categoria")
    
    #return "Cliente agregado exitosamente a la nueva categoria" #Muestro un mensaje de éxito si se creó el registro
    return client

#Detalle de cliente con id pasado por URL. Con sus cuentas y categorias.
@cliente.get("/clientes/cuentas/{account_id}",response_model=schema_accounts.CuentaSaldo, status_code=200)
def read_clientDetail(account_id: int, db: Session = Depends(get_db)):
    #Obtengo el saldo total de la cuenta, tanto en pesos como en dolares
    cuenta = crud_accounts.get_clientBalance(db, account_id = account_id) 

    if cuenta is None: 
        #Si no se pudo crear y no se lanzó alguna excepción durante la ejecución de get_clientBalance informo la situación
        raise HTTPException(status_code=404, detail="Cuenta no existente")
    
    return cuenta #Retorno la variable cuenta para mostrar los resultados en el navegador.