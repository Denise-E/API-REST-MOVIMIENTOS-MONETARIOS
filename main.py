from fastapi import FastAPI

from router.cliente import cliente
from router.movimiento import movimiento
from config.database import engine, metaData
from models import Cliente, Categoria, Categoria_Cliente, Cuenta, Movimiento, Tipo_Movimiento;

Cliente.Base.metadata.create_all(bind=engine)
Categoria.Base.metadata.create_all(bind=engine)
Categoria_Cliente.Base.metadata.create_all(bind=engine)
Cuenta.Base.metadata.create_all(bind=engine)
Movimiento.Base.metadata.create_all(bind=engine)
Tipo_Movimiento.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(cliente)
app.include_router(movimiento)
