from fastapi.testclient import TestClient
from main import app

test = TestClient(app)

# TEST RUTAS MOVIMIENTO ROUTER

#Ver un movimiento en concreto
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


#Creacion de un movimiento
'''def test_create_mov_incomeOk(): 
    response = test.post("/movimientos", json = { #Ingreso en cuenta existente
        "id_cuenta": 5,
        "tipo": 1,
        "importe": 230000,
        "fecha": "2023-07-17T13:07:14.553Z"
        }) 
    assert response.status_code == 200
    assert response.json() == {
            "id_cuenta": 5,
            "tipo": 1,
            "importe": 230000,
            "fecha": "2023-07-17T13:07:14"
        }'''


'''def test_create_mov_outflowOk(): 
    response = test.post("/movimientos", json = { #Egreso en cuenta existente con saldo
            "id_cuenta": 5,
            "tipo": 2,
            "importe": 200,
            "fecha": "2023-07-17T13:07:14.553Z"
        }) 
    assert response.status_code == 200
    assert response.json() == {
            "id_cuenta": 5,
            "tipo": 2,
            "importe": 200,
            "fecha": "2023-07-17T13:07:14"
        }'''
    
def test_create_mov_outflow_insuficientMoney(): 
    response = test.post("/movimientos", json = { #Egreso, sin alcanzar el saldo
            "id_cuenta": 5,
            "tipo": 2,
            "importe": 1000000,
            "fecha": "2023-07-17T13:07:14.553Z"
        }) 
    assert response.status_code == 404
    assert response.json() == {
            "detail": "Saldo insuficiente"
        }

def test_create_mov_invalid_accountId(): 
    response = test.post("/movimientos", json = { #Movimiento a id_cuenta inexistente
            "id_cuenta": 99,
            "tipo": 2,
            "importe": 200,
            "fecha": "2023-07-17T13:07:14.553Z"
        }) 
    assert response.status_code == 404
    assert response.json() == {
        "detail": "No existe una cuenta con el ID solicitado"
    }

def test_create_mov_invalid_accountId():  
    response = test.post("/movimientos", json = { #Tipo de movimiento inexistente (id pasado) 
            "id_cuenta": 5,
            "tipo": 9,
            "importe": 200,
            "fecha": "2023-07-17T13:07:14.553Z"
        }) 
    assert response.status_code == 404
    assert response.json() =={
            "detail": "No existe el tipo de movimiento solicitado"
        }

# Eliminacion de un movimiento.
'''def test_delete_mov():
    response = test.delete("/movimientos/17") #Pasandole un id válido   #Para que no se elimine cada que vez que pruebo tests
    assert response.status_code == 200
    assert response.json() == {
            "id": 17,
            "id_cuenta": 1,
            "tipo": 2,
            "importe": 1000,
            "fecha": "2023-07-17T15:01:11"
        }'''
    
def test_delete_mov():
    response = test.delete("/movimientos/40") #Pasandole un id inválido
    assert response.status_code == 404
    assert response.json() == {
            "detail": "Movimiento no encontrado"
        }
    



# TEST RUTAS CLIENTE ROUTER

#Listado de todos los clientes
'''def test_read_clients(): 
    response = test.get("/clientes")
    assert response.status_code == 200                        #Actualizar con regustros finales BBDD
    assert response.json() == [
        {
            "id": 1,
            "dni": 11111111,
            "nombre": "Denise Eichenblat"
        },
        {
            "id": 4,
            "dni": 12987335,
            "nombre": "Jose Mauro"
        },
        {
            "id": 5,
            "dni": 98654332,
            "nombre": "Martina Diaz"
        },
        {
            "id": 6,
            "dni": 42588971,
            "nombre": "Bart Simpson"
        },
        {
            "id": 10,
            "dni": 23232323,
            "nombre": "Nancy Gimenes"
        },
        {
            "id": 12,
            "dni": 99999999,
            "nombre": "Fausto Banza"
        },
        {
            "id": 13,
            "dni": 2147483647,
            "nombre": "Fausto Banza"
        }
        ]
'''

#Ver detalle de un cliente en concreto
def test_read_client():
    response = test.get("/clientes/1") #Pasandole un id válido
    assert response.status_code == 200
    assert response.json() == {
            "id": 1,
            "dni": 11111111,
            "nombre": "Denise Eichenblat",
            "categorias": [
                "Preferencial",
                "Estandar"
            ],
            "cuentas": [
                {
                "IDs": [
                    1,
                    5,
                    6
                ]
                }
            ]
        }

def test_read_client_incorrectId():
    response = test.get("/clientes/90") #Pasandole un id inexistente en la base de datos
    assert response.status_code == 404
    assert response.json() =={
        "detail": "Cliente no existente"
        }   

#Creacion de un cliente
'''def test_create_client():
    response = test.post("/clientes", json = { #Cliente no registrado previamente
            "dni": 33653422,
            "nombre": "Facundo Jasin",
            "categorias": [
                0
            ],
            "cantCuentas": 0
        }) 
    assert response.status_code == 200
    assert response.json() ==    {
        "id": 16,
        "dni": 33653422,
        "nombre": "Facundo Jasin"
    }'''


def test_create_client_alreadyRegister():
    response = test.post("/clientes", json = { #Cliente ya registrado previamente segun su DNI
            "dni": 99999999,
            "nombre": "Fausto Banza",
            "categorias": [
                0
            ],
            "cantCuentas": 0
        }) 
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Ya existe un cliente registrado con el DNI ingresado"
        }
    
