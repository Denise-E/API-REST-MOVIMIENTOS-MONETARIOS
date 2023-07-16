from fastapi import HTTPException
from sqlalchemy.orm import Session
import models.Cliente as model
import models.Categoria_Cliente as model_categoriaCliente
from schemas import ClienteSchema as schema
from schemas import Categoria_ClienteSchema as schema_clientCategory
from crud import categorias as crud_categorias
from crud import cuentas as crud_cuentas


def get_clients(db: Session, skip: int = 0):
    return db.query(model.Cliente).offset(skip).all()

def get_clientById(db: Session,client_id: int):
    return db.query(model.Cliente).filter(model.Cliente.id == client_id).first()

def get_clientByDni(db: Session,client_dni: int):
    return db.query(model.Cliente).filter(model.Cliente.dni == client_dni).first()

def get_clientDetail(db: Session,client_id: int):
    client = get_clientById(db,client_id)
    clientDetail = None

    if client is not None:
        client_category = crud_categorias.get_categoriesByClient_detail(db,client.id)
        client_account = crud_cuentas.get_accountsByClient_detail(db,client.id)
        clientDetail = schema.ClienteDetail(id = client.id, dni = client.dni, nombre =client.nombre, categorias = client_category, cuentas = client_account)
     
    return clientDetail


def create_mov(db: Session, data:schema.ClienteCreate):
    client = get_clientByDni(db, data.dni) #Valido que no exista ya el cliente por DNI
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
    
    client = get_clientById(db, client_id=client_id)

    if client is not None:
        crud_categorias.delete_clientCategories(db,client.id)
        crud_cuentas.delete_clienteAccounts(db,client.id)
        db.delete(client)
        db.commit()

    return client


#VERIFICAR QUE NO ESTE YA EN ESA CATEGORIA Y QUE EXISTA LA CATEGORIA
def add_clientToCategory(data:schema_clientCategory.Categoria_ClienteCreate,db: Session,client_id: int):
    #Primero valido que exista el cliente por el id pasado por URL
    client = get_clientById(db, client_id=client_id)

    if client is None:
        raise HTTPException(status_code=404, detail="No se encontro al cliente")
    
    '''Si existe el cliente, desde categorias valido id de la catgeoria valido y que el ususario no este 
    asociado ya a esa categoria'''
    crud_categorias.validateCategoryForClient(db, client_id=client_id, cat_id = data.id_categoria)

    #Si esta todo ok agregao el registro a la tabla cliente_categoria
    new_category = model_categoriaCliente.Categoria_Cliente(id_categoria = data.id_categoria, id_cliente = client_id)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category
