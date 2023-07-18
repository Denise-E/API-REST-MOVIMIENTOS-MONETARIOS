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
def test_create_mov_incomeOk(): 
    response = test.post("/movimientos", json = { #Ingreso en cuenta existente
        "id_cuenta": 5,
        "tipo": 1,
        "importe": 230000
        }) 
    assert response.status_code == 201
    assert response.json() == {
            "id_cuenta": 5,
            "tipo": 1,
            "importe": 230000
        }


def test_create_mov_outflowOk(): 
    response = test.post("/movimientos", json = { #Egreso en cuenta existente con saldo
            "id_cuenta": 5,
            "tipo": 2,
            "importe": 200
        }) 
    assert response.status_code == 201
    assert response.json() == {
            "id_cuenta": 5,
            "tipo": 2,
            "importe": 200
        }
    

def test_create_mov_outflow_insuficientMoney(): 
    response = test.post("/movimientos", json = { #Egreso, sin alcanzar el saldo
            "id_cuenta": 5,
            "tipo": 2,
            "importe": 1000000
        }) 
    assert response.status_code == 400
    assert response.json() == {
            "detail": "Saldo insuficiente"
        }

def test_create_mov_invalid_accountId(): 
    response = test.post("/movimientos", json = { #Movimiento a id_cuenta inexistente
            "id_cuenta": 99,
            "tipo": 2,
            "importe": 200
        }) 
    assert response.status_code == 400
    assert response.json() == {
            "detail": "No existe una cuenta con el ID solicitado"
        }


def test_create_mov_invalid_accountId():  
    response = test.post("/movimientos", json = { #Tipo de movimiento inexistente (id pasado) 
            "id_cuenta": 5,
            "tipo": 9,
            "importe": 200
        }) 
    assert response.status_code == 400
    assert response.json() =={
            "detail": "No existe el tipo de movimiento solicitado"
        }

def test_create_mov_invalid_mount():  
    response = test.post("/movimientos", json = { #Importe menor o igual a  0
            "id_cuenta": 5,
            "tipo": 1,
            "importe": 0
        }) 
    assert response.status_code == 400
    assert response.json() =={
            "detail": "Ingrese un monto valido"
        }

# Eliminacion de un movimiento.
def test_delete_mov():
    response = test.delete("/movimientos/17") #Pasandole un id válido   #Para que no se elimine cada que vez que pruebo tests
    assert response.status_code == 200
    assert response.json() == {
            "id": 17,
            "id_cuenta": 1,
            "tipo": 2,
            "importe": 1000,
            "fecha": "2023-07-17T15:01:11"
        }
    
def test_delete_mov():
    response = test.delete("/movimientos/40") #Pasandole un id inválido
    assert response.status_code == 404
    assert response.json() == {
            "detail": "Movimiento no encontrado"
        }
    



# TEST RUTAS CLIENTE ROUTER

#Listado de todos los clientes
def test_read_clients(): 
    response = test.get("/clientes")
    assert response.status_code == 200         
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
def test_create_client():
    response = test.post("/clientes", json = { #Cliente no registrado previamente
            "dni": 33653422,
            "nombre": "Facundo Jasin",
            "categorias": [
                0
            ],
            "cantCuentas": 0
        }) 
    assert response.status_code == 201
    assert response.json() ==    {
        "id": 16,
        "dni": 33653422,
        "nombre": "Facundo Jasin"
    }


def test_create_client_alreadyRegister():
    response = test.post("/clientes", json = { #Cliente ya registrado previamente segun su DNI
            "dni": 99999999,
            "nombre": "Fausto Banza",
            "categorias": [
                0
            ],
            "cantCuentas": 0
        }) 
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Ya existe un cliente registrado con el DNI ingresado"
        }

def test_create_client_invalid_dni():
    response = test.post("/clientes", json = { #DNI invalido
            "dni": 0,
            "nombre": "Fausto Banza",
            "categorias": [
                0
            ],
            "cantCuentas": 0
        }) 
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Ingrese un dni valido"
        }

def test_create_client_invalid_name():
    response = test.post("/clientes", json = { #Nombre invalido
            "dni": 23536277,
            "nombre": "",
            "categorias": [
                0
            ],
            "cantCuentas": 0
        }) 
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Ingrese un nombre valido"
        }

#Actualizacion de los datos de un cliente en particular
def test_update_client():
    response = test.put("/clientes/4", json = { #Modificacion realizada, id valido
            "dni": 12987335, 
            "nombre": "Jose Maurro" 
        }) 
    assert response.status_code == 200
    assert response.json() ==    {
        "id": 4,
        "dni": 12987335,
        "nombre": "Jose Maurro"
    }

def test_update_client_invalidId():
    response = test.put("/clientes/90", json = { #Id invalido
            "dni": 22222222, 
            "nombre": "Jose Gomez" 
        }) 
    assert response.status_code == 404
    assert response.json() == {
            "detail": "No existe cliente con el id solicitado"
        }
    

def test_update_client_invalid_dni():
    response = test.put("/clientes/1", json = { #DNI invalido
            "dni": 0, 
            "nombre": "Jose Gomez" 
        }) 
    assert response.status_code == 400
    assert response.json() == {
            "detail": "Ingrese un dni valido"
        }


def test_update_client_invalid_name():
    response = test.put("/clientes/1", json = { #Nombre invalido
            "dni": 89876554, 
            "nombre": "" 
        }) 
    assert response.status_code == 400
    assert response.json() == {
            "detail": "Ingrese un nombre valido"
        }

#Eliminacion de un cliente
def test_delete_client():
    response = test.delete("/clientes/13")  #Id valido
    assert response.status_code == 200
    assert response.json() ==  {
            "id": 13,
            "dni": 2147483647,
            "nombre": "Fausto Banza"
        }

def test_delete_client_invalidId():
    response = test.delete("/clientes/80")  #Id invalido
    assert response.status_code == 404
    assert response.json() == {
            "detail": "Cliente no encontrado"
        }
    

#Agregar cliente a una categoria
def test_add_clientToCategory():
    response = test.post("/clientes/categorias/5", json = { #Id cliente y categoria valida
                "id_categoria": 1
        }) 
    assert response.status_code == 201
    assert response.json() == {
            "id_categoria": 1,
            "id_cliente": 5
        }

def test_add_clientToCategory_alreadyRegister():
    response = test.post("/clientes/categorias/10", json = { #Cliente ya registrado previamente en la categoria solicitada
            "id_categoria": 1
        }) 
    assert response.status_code == 400
    assert response.json() == {
            "detail": "El cliente ya esta en la categoria solicitada"
        }

def test_add_clientToCategory_invalidClientId():
    response = test.post("/clientes/categorias/80", json = { #Id del cliente invalido
            "id_categoria": 2
        }) 
    assert response.status_code == 404
    assert response.json() == {
            "detail": "No se encontro al cliente"
        }

def test_add_clientToCategory_invalidCategoryId():
    response = test.post("/clientes/categorias/5", json = { #Id de la categoria invalido
            "id_categoria": 9
        }) 
    assert response.status_code == 400
    assert response.json() == {
            "detail": "No existe la categoria buscada"
        }
    

#Ver saldos de una cuenta en especifico
def test_read_clientDetail():
    response = test.get("/clientes/cuentas/1") #Pasandole un id válido
    assert response.status_code == 200
    assert response.json() == {
        "saldo_ARS": 219300.0,
        "saldo_USD": 108601746.0
    }


def test_read_clientDetail_invalidId():
    response = test.get("/clientes/cuentas/90") #Pasandole un id inválido
    assert response.status_code == 404
    assert response.json() == {
        "detail": "No existe una cuenta con el ID solicitado"
    }
