from fastapi import APIRouter, HTTPException, Response
from fastapi import Depends
from config.database import SessionLocal
from sqlalchemy.orm import Session
from crud import movimientos as crud

from schemas import MovimientoSchema as schema
from models import Movimiento as model

movimiento = APIRouter()

# DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@movimiento.get("/movimientos/{mov_id}", response_model=schema.Movimiento)
def read_mov(mov_id: int, db: Session = Depends(get_db)):
    db_mov = crud.get_mov(db, mov_id=mov_id)

    if db_mov is None:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    print(db_mov)
    return db_mov

@movimiento.delete("/movimientos/{mov_id}", response_model=schema.Movimiento)
def delete_mov(mov_id: int, db: Session = Depends(get_db)):
    db_mov = crud.delete_mov(db, mov_id=mov_id)

    if db_mov is None:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")

    return db_mov