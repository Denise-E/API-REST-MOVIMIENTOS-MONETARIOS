from fastapi import APIRouter #Para dividir las rutas de la app

cliente = APIRouter()

@cliente.get("/clientes")
def root():
    return "Router mov"