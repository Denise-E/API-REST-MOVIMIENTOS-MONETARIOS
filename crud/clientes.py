from fastapi import HTTPException
from sqlalchemy.orm import Session

import models.Cliente as model
import models.Categoria_Cliente as model_categoriaCliente
from schemas import ClienteSchema as schema
from schemas import Categoria_ClienteSchema as schema_clientCategory
from crud import categorias as crud_categorias
from crud import cuentas as crud_cuentas
from crud import gral_validations as validations

#Obtengo todos los clientes registrados en mi base de datos
def get_clients(db: Session, skip: int = 0):
    return db.query(model.Cliente).offset(skip).all()

#Obtengo al cliente de mi base de datos que posee el id pasado por url y recibidó en la función por parámetro
def get_clientById(db: Session,client_id: int):
    return db.query(model.Cliente).filter(model.Cliente.id == client_id).first()

#Obtengo al cliente de mi base de datos que posee el dni recibidó en la función por parámetro
def get_clientByDni(db: Session,client_dni: int):
    return db.query(model.Cliente).filter(model.Cliente.dni == client_dni).first()

#Retorna un objeto ClienteDetail, el cual contiene datos del cliente junto a sus cuentas y categorias
def get_clientDetail(db: Session,client_id: int):
    client = get_clientById(db,client_id) #Busco el cliente por id
    clientDetail = None

    if client is not None: #Si existe el cliente en la base de datos
        client_category = crud_categorias.get_categoriesByClient_detail(db,client.id) #Obtengo las categorias a las cuales está asociado el cliente
        client_account = crud_cuentas.get_accountsByClient_detail(db,client.id) #Obtengo todas las cuentas del cliente
        #Creo el objeto a retornar, con todos los datos obtenidos.
        clientDetail = schema.ClienteDetail(id = client.id, dni = client.dni, nombre =client.nombre, categorias = client_category, cuentas = client_account)
     
    return clientDetail


def create_client(db: Session, data:schema.ClienteCreate):
    client = get_clientByDni(db, data.dni) #Valido que no exista ya el cliente por DNI
    new_client = None

    if client is not None: #Si el cliente ya está registrado lo informo.
        raise HTTPException(status_code=404, detail="Ya existe un cliente registrado con el DNI ingresado")
    

    #Si el cliente no estaba registrado valido los datos antes de crearlo 
    validations.validate_client_dni(data.dni)
    validations.validate_client_name(data.nombre)

    #Mismo proceso deberia hacerlo con el modelo de las tablas cuentas y categorias
    new_client = model.Cliente(dni = data.dni, nombre = data.nombre) #Creo el modelo del cliente
    #Lo agrego a la base de datos y me aseguro de persistir los cambios.
    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    return new_client #Devuelvo al cliente creado

#Actualizacion del Cliente. Solamente puede actualizarse su nombre y dni, no las cuestas y categorias a la cual se lo asocia.
def update_client(client_id: int, data:schema.Cliente,db: Session):
    client = get_clientById(db,client_id) #Verifico que exista un cliente con el id solicitado en mi base de datos

    if client is None: #Si no existe lo informo
        raise HTTPException(status_code=404, detail="No existe cliente con el id solicitado")
    
    #Si existia, primero valido sus datos y si pasan la validacion los modifico
    validations.validate_client_dni(data.dni)
    validations.validate_client_name(data.nombre)
    client.dni = data.dni
    client.nombre = data.nombre

    #Lo actualizo en la base de datos y me aseguro de persistir los cambios.
    db.commit()
    db.refresh(client)

    return client

#Eliminación del cliente en la base de datos
def delete_client(db: Session, client_id: int):
    client = get_clientById(db, client_id=client_id) #Verifico que exista el cliente con el id solicitado

    if client is not None: #Si existe el cliente....
        crud_categorias.delete_clientCategories(db,client.id) #Elimino todos los registros asociados en la tabla intermedia categorias_clientes
        crud_cuentas.delete_clienteAccounts(db,client.id) #Elimino todas las cuentas del cliente
        #Elimino al cliente y y me aseguro de persistir los cambios.
        db.delete(client)
        db.commit()

    return client #Devuelvo al cliente eliminado


#Agrega al cliente a una nueva categoria. Agrega registro en la tabla intermedia categoria_cliente
def add_clientToCategory(data:schema_clientCategory.Categoria_ClienteCreate,db: Session,client_id: int):
    #Primero valido que exista el cliente con el id pasado por URL
    client = get_clientById(db, client_id=client_id)

    if client is None: #Si no existe cliente con tal id lo informo
        raise HTTPException(status_code=404, detail="No se encontro al cliente")
    
    '''
    Si existe el cliente, desde categorias valido que el id de la catgeoria sea valido y que el ususario no 
    este asociado ya a esa categoria
    '''
    crud_categorias.validateCategoryForClient(db, client_id=client_id, cat_id = data.id_categoria)

    #Si esta todo ok agrego el registro a la tabla cliente_categoria
    new_category = model_categoriaCliente.Categoria_Cliente(id_categoria = data.id_categoria, id_cliente = client_id)
    #Agreo el registro y me asgeuro de que la base de datos quede actualizada
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category #Retorno el registro creado
