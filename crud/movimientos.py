from sqlalchemy.orm import Session
import models.Movimiento as model
from schemas import MovimientoSchema as schema

def get_mov(db: Session, mov_id: int):
    return db.query(model.Movimiento).filter(model.Movimiento.id == mov_id).first()

def create_mov(db: Session, data:schema.MovimientoCreate):
    new_mov = model.Movimiento(id_cuenta = data.id_cuenta, tipo = data.tipo, importe = data.importe, fecha = data.fecha)
    db.add(new_mov)
    db.commit()
    db.refresh(new_mov)
    return new_mov

def delete_mov(db: Session, mov_id: int):
    mov = get_mov(db, mov_id=mov_id)

    if mov is not None:
        db.delete(mov)
        db.commit()
        
    return mov
