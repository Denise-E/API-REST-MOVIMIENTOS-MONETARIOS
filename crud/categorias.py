from fastapi import HTTPException
from sqlalchemy.orm import Session
import models.Categoria_Cliente as model
import models.Categoria as model_categoria

#Obtengo todas las categorias de un cliente, buscando por su id
def get_categoriesByClient(db: Session,client_id: int):
    return db.query(model.Categoria_Cliente).filter(model.Categoria_Cliente.id_cliente == client_id).all()
    

#Devuelve una lista con los nombres de las categorias a las cuales pertenece un cliente
def get_categoriesByClient_detail(db: Session,client_id: int):
    cat = get_categoriesByClient(db,client_id) #Obtengo todas las categorias
    finalList = [] #Creo lista auxiliar, la cual estará devolviendo la función
    
    #Para acceder solo al nombre de la categoria, sin mostrar el id del cliente que me llega en el objeto
    for i in range(len(cat)): 
        finalList.append(getCategoryName(db,cat[i].id_categoria))


    return finalList

#Obtengo la categoria correspondiente con el numero de id pasado por parametro
def get_categoryById(db: Session,category_id: int):
    category = db.query(model_categoria.Categoria).filter(model_categoria.Categoria.id == category_id).first()
    
    if category is None: #Si no existe la categoria lo informo
        raise HTTPException(status_code=400, detail="No existe la categoria buscada")
    
    return category #Si existe la categoria la devuelvo


#Devuelve el nombre de la categoria cuyo id pasaron por parametro
def getCategoryName(db: Session, category_id: int):
    category = get_categoryById(db,category_id) #Busco la categoria por id
    return category.nombre #Devuelvo únicamnete el nombre de la categoria encontrada
    #Si la categoria no se encontró el metodo llamado en la linea 34 lanza una excepción, por lo cual no se ejecutará el return

'''
Elimina todas las asociaciones de un cliente con sus categorias. 
Todos los registros de ese cliente de la tabla intermeda categorias_cliente
'''
def delete_clientCategories(db: Session, client_id: int):
    categories = get_categoriesByClient(db,client_id) #Obtengo todas las categorias del cliente

    if categories is not None: #Si hay registros elimino cada uno de estos y persisto los cambios en la base de datos
        for i in range(len(categories)):
            db.delete(categories[i])
            db.commit()

    return categories


#Valida que el id de la categoria sea válido y que el usuario no este asociado ya a esa categoria
#Este metodo es usado al agregar al cliente a una categoria
def validateCategoryForClient(db: Session, client_id:int, cat_id: int):
    get_categoryById(db,cat_id) #Verifica que exista una categoria con el id solicitado, si no la hay lanza una excepcion

    '''
    Si existe la categoria (no se lanzo una excepcion), verifico que el usuario no este ya asociado 
    a esa categoria. Si lo está lanzo excepción.
    '''
    clientCategories = get_categoriesByClient(db, client_id)
    if any(cat.id_categoria == cat_id for cat in clientCategories):
        raise HTTPException(status_code=400, detail="El cliente ya esta en la categoria solicitada")
