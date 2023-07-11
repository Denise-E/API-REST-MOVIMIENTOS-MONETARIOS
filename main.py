from fastapi import Depends, FastAPI, HTTPException, Request, Response
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

@app.get("/cuentas/{cliente_id}", response_model=list[schemas.Movimiento]) #Para verificar para poder eliminar clientes con sus cuentas
def read_cuenta(cliente_id: int, db: Session = Depends(get_db)):
    cuentas = crud.get_cuentasPorClientes(db,cliente_id = cliente_id )
    return cuentas

@app.get("/clientes/{cliente_id}", response_model=schemas.Cliente)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = crud.get_cliente(db, cliente_id=cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@app.delete("/clientes/{cliente_id}", response_model=list[schemas.Cliente]) 
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = crud.delete_cliente(db, cliente_id = cliente_id)
    return cliente

@app.post("/clientes/", response_model=schemas.Cliente)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)): #Tendria que reestructurar la BBDD y agregar dni para diferenciarlos por ese dato unico
    return crud.create_cliente(db=db, cliente=cliente)


'''@app.put("/clientes/{cliente_id}", response_model=schemas.Cliente) #IN PROCESSS
def update_cliente(cliente_id: int,nombre: str, cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_user = crud.get_cliente(db, cliente_id=cliente_id)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)'''

@app.get("/movimientos/{movimiento_id}", response_model=schemas.Movimiento) #Devuelve solo ID, CHEQUEAR SCHEMA
def read_movimiento(movimiento_id: int, db: Session = Depends(get_db)):
    movimiento = crud.get_movimiento(db, movimiento_id=movimiento_id)
    if movimiento is None:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return movimiento

@app.delete("/movimientos/{movimiento_id}", response_model=list[schemas.Cliente]) 
def eliminar_movimiento(movimiento_id: int, db: Session = Depends(get_db)):
    cliente = crud.delete_movimiento(db, movimiento_id = movimiento_id)
    return cliente