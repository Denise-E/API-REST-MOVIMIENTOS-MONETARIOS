from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session

from router.cliente import cliente
from config.database import SessionLocal, engine, metaData
from models import Cliente, Categoria, Categoria_Cliente, Cuenta, Movimiento, Tipo_Movimiento;

Cliente.Base.metadata.create_all(bind=engine)
Categoria.Base.metadata.create_all(bind=engine)
Categoria_Cliente.Base.metadata.create_all(bind=engine)
Cuenta.Base.metadata.create_all(bind=engine)
Movimiento.Base.metadata.create_all(bind=engine)
Tipo_Movimiento.Base.metadata.create_all(bind=engine)

app = FastAPI()

# DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(cliente)
