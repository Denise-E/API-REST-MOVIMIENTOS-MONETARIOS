from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/clientes", response_model=list[schemas.Cliente])
def read_clients(skip: int = 0, db: Session = Depends(get_db)):
    clientes = crud.get_clientes(db, skip=skip)
    return clientes


@app.get("/movimientos/{movimiento_id}", response_model=schemas.Movimiento) #Devuelve solo ID
def read_movimiento(movimiento_id: int, db: Session = Depends(get_db)):
    db_movimiento = crud.get_movimiento(db, movimiento_id=movimiento_id)
    if db_movimiento is None:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return db_movimiento