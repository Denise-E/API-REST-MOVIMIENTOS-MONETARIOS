from sqlalchemy.orm import Session
import models.Movimiento as model

def get_mov(db: Session, mov_id: int):
    return db.query(model.Movimiento).filter(model.Movimiento.id == mov_id).first()

def delete_mov(db: Session, mov_id: int):
    mov = get_mov(db, mov_id=mov_id)
    db.delete(mov)
    db.commit()
    return mov
