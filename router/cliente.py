from fastapi import APIRouter #Para dividir las rutas de la app

cliente = APIRouter()

@cliente.get("/")
def root():
    return "Router clientes"