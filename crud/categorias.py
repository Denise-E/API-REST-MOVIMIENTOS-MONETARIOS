from fastapi import HTTPException
from sqlalchemy.orm import Session
import models.Categoria_Cliente as model
import models.Categoria as model_categoria


def get_categoriasPorCliente(db: Session,client_id: int):
    cat = db.query(model.Categoria_Cliente).filter(model.Categoria_Cliente.id_cliente == client_id).all()
    finalList = []
    
    #Para acceder solo al nombre de la categoria, sin mostrar el id del cliente
    for i in range(len(cat)): 
        finalList.append(getNombreCategoria(db,cat[i].id_categoria))


    return finalList
    

def getNombreCategoria(db: Session, category_id: int):
    category = db.query(model_categoria.Categoria).filter(model_categoria.Categoria.id == category_id).first()
    
    if category is None:
        raise HTTPException(status_code=404, detail="No existe la categoria buscada")

    return category.nombre
