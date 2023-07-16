from fastapi import HTTPException
from sqlalchemy.orm import Session
import models.Cuenta as model
from schemas import CuentaSchema as schema
from crud import movimientos as crud_movimientos
import requests

#Obtengo todas las cuentas del cliente cuyo id pasaron por parametro
def get_accountsByClient(db: Session,client_id: int):
    return db.query(model.Cuenta).filter(model.Cuenta.id_cliente == client_id).all()

#Obtengo una cuenta por su id
def get_accountById(db: Session,account_id: int):
    return db.query(model.Cuenta).filter(model.Cuenta.id == account_id).first()

#Devuelve una lista con el id de todas las cuentas asociadas al cliente cuyo id pasaron por parametro
def get_accountsByClient_detail(db: Session,client_id: int):
    account = get_accountsByClient(db, client_id) #Obtiene todas las cuentas del cliente
    finalList = [{"IDs": []}]

    #Para acceder solo al id de la cuenta, sin mostrar el id del cliente.
    for i in range(len(account)): 
        finalList[0]["IDs"].append(account[i].id)

    return finalList 
    
#Elimina todas las cuentas asociadas a un cliente
def delete_clienteAccounts(db: Session, client_id: int):    
    accounts = get_accountsByClient(db, client_id) #Busco todas las cuentas del cliente por el id pasado por parametro

    if accounts is not None:
        for i in range(len(accounts)): #Recorro la lista con las cuentas
            #Voy eliminando de a una y persistiendo los cambios en la base de datos
            db.delete(accounts[i])
            db.commit()

    return accounts

 
#Devuelve un objeto con el saldo final de la cuenta al día de la fecha, tanto en pesos como en dolares
def get_clientBalance(db: Session, account_id: int):
    account = get_accountById(db, account_id) #Obtiene una cuenta por su id

    if account is None: #Si no existe una cuenta con el id buscado lo informa
        raise HTTPException(status_code=404, detail="No existe una cuenta con el ID solicitado")

    #Obtengo todos los movimientos de la cuenta solicitada por id
    movements = crud_movimientos.get_movementsByAccount(db, account_id)
    totalARS = 0
    totalUSD = 0

    #Filtro la lista de movimientos, sumando y restando segun corresponda para obtener el saldo total en ARS
    if movements is not None:
        for i in range(len(movements)):
            if movements[i].tipo == 1:
                totalARS += movements[i].importe #Ingreso. Sumo el importe registrado a totalArs
            else: 
                totalARS -= movements[i].importe #Egreso. Resto el importe registrado a totalArs
        
        totalUSD = get_total_usd(totalARS) #Llamo al método que me va a obtener el valor en USD segun la cotización solicitada

    clientBalance = schema.CuentaSaldo(saldo_ARS = totalARS, saldo_USD = totalUSD) #Armo el objeto que va a ser mostrado en el navegador
    return clientBalance

#Recibe el saldo total de la cuenta en pesos y devuelve el valor en dólares consumiendo la API con la cotización actualizada.
def get_total_usd(totalARS: float):
    usd_value = 0

    response_API = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales')
    data = response_API.json() #Accedo a todo el array que contiene la api en formato json para poder trabajarlo
    
    #Busco el objeto dentro de la lista data con nombre = Dolar Bolsa
    cont = 0
    encontrado = False
   
    while encontrado is False and cont < len(data):
        if data[cont]["casa"]["nombre"] == "Dolar Bolsa":
            encontrado = True
            usd_value = data[cont]["casa"]["venta"] #Me guardo la cotizacion del dolar venta en una variable

        cont+=1

    #Formatea usd_value que llega como string con coma para poder transformarlo a float
    float_usd = usd_value.replace(",", ".")
    #print("USD" , float_usd)

    #Multiplico total obtenido en pesos por la cotizacion dolar venta de Dolar Bolsa
    totalUSD = totalARS * float(float_usd)
    return totalUSD