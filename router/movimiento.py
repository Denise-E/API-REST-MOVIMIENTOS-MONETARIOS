from fastapi import APIRouter, HTTPException
from fastapi import Depends
from config.database import SessionLocal
from sqlalchemy.orm import Session

from crud import movimientos as crud
from schemas import MovimientoSchema as schema


movimiento = APIRouter()

# DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        
#Ruta para acceder por URL al detalle del movimiento con id especificado en la url, en caso de existir.
@movimiento.get("/movimientos/{mov_id}",response_model=schema.Movimiento) 
def read_mov(mov_id: int, db: Session = Depends(get_db)):
    db_mov = crud.get_mov(db, mov_id=mov_id) #Busco el movimiento por ID

    if db_mov is None: #Si no existe un movimiento con el id solicitado lanzo excepción con status 404
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    
    return db_mov #Si exitió un movimiento, no se lanzó la excepción y este se verá en el navegador.


#Ruta para la creación de un movimiento (Ingreso o Egreso de dinero a una cuenta)
@movimiento.post("/movimientos",response_model=schema.MovimientoCreate,status_code=201)
def create_mov(input: schema.MovimientoCreate,db: Session = Depends(get_db)):
    new_mov = crud.create_mov(db, input) #Creo el movimiento

    if new_mov is None: #Si me retornó None, no se pudo efectuar el movimiento y lanzo excepción avisandolo.
        raise HTTPException(status_code=400, detail="No se pudo registrar el movimiento")
    
    return new_mov #Si se creó, muestro el registro creado.


#Ruta para eliminar un movimiento por su id
@movimiento.delete("/movimientos/{mov_id}",response_model=schema.Movimiento)
def delete_mov(mov_id: int, db: Session = Depends(get_db)):
    db_mov = crud.delete_mov(db, mov_id=mov_id) #Elimino el movimiento

    if db_mov is None: #Si no pudo eliminarse, db_mov valdrá none e informe el error con una excepción.
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")

    return db_mov #Si se logró la accioón deseada, devuelvo el movimiento eliminado