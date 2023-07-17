from fastapi.testclient import TestClient
#from router.movimiento import movimiento
from main import app

test = TestClient(app)

# Test rutas movimiento router
def test_read_mov():
    response = test.get("/movimientos/14") #Pasandole un id válido
    assert response.status_code == 200
    assert response.json() == {
        "id": 14,
        "id_cuenta": 1,
        "tipo": 1,
        "importe": 230500.0,
        "fecha": "2023-07-15T18:04:45"
    }

def test_read_mov_incorrectId():
    response = test.get("/movimientos/1") #Pasandole un id inexistente en la base de datos
    assert response.status_code == 404
    assert response.json() =={
    "detail": "Movimiento no encontrado"
    }

