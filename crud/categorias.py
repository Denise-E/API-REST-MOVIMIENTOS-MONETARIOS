from fastapi import HTTPException
from sqlalchemy.orm import Session
import models.Categoria_Cliente as model
import models.Categoria as model_categoria


def get_categoriesByClient(db: Session,client_id: int):
    return db.query(model.Categoria_Cliente).filter(model.Categoria_Cliente.id_cliente == client_id).all()
    

def get_categoriesByClient_detail(db: Session,client_id: int):
    cat = get_categoriesByClient(db,client_id)
    finalList = []
    
    #Para acceder solo al nombre de la categoria, sin mostrar el id del cliente
    for i in range(len(cat)): 
        finalList.append(getCategoryName(db,cat[i].id_categoria))


    return finalList


def getCategoryName(db: Session, category_id: int):
    category = db.query(model_categoria.Categoria).filter(model_categoria.Categoria.id == category_id).first()
    
    if category is None:
        raise HTTPException(status_code=404, detail="No existe la categoria buscada")

    return category.nombre

def delete_clientCategories(db: Session, client_id: int):
    categories = get_categoriesByClient(db,client_id)

    if categories is not None:
        for i in range(len(categories)):
            db.delete(categories[i])
            db.commit()

    return categories


def validateCategoryForClient(db: Session, client_id:int, cat_id: int):
    return None