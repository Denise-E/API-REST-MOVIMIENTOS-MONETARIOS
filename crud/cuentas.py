from fastapi import HTTPException
from sqlalchemy.orm import Session
import models.Cuenta as model
from schemas import CuentaSchema as schema
from crud import movimientos as crud_movimientos
import requests


def get_accountsByClient(db: Session,client_id: int):
    return db.query(model.Cuenta).filter(model.Cuenta.id_cliente == client_id).all()

def get_accountById(db: Session,account_id: int):
    return db.query(model.Cuenta).filter(model.Cuenta.id == account_id).first()

def get_accountsByClient_detail(db: Session,client_id: int):
    account = get_accountsByClient(db, client_id)
    finalList = [{"IDs": []}]

    #Para acceder solo al id de la cuenta, sin mostrar el id del cliente.
    for i in range(len(account)): 
        finalList[0]["IDs"].append(account[i].id)

    return finalList 
    

def delete_clienteAccounts(db: Session, client_id: int):    
    accounts = get_accountsByClient(db, client_id)

    if accounts is not None:
        for i in range(len(accounts)):
            db.delete(accounts[i])
            db.commit()

    return accounts

 
#Devuelve un objeto con el saldo final de la cuenta al día de la fecha, tanto en pesos como en dolares
def get_clientBalance(db: Session, account_id: int):
    account = get_accountById(db, account_id)

    if account is None:
        raise HTTPException(status_code=404, detail="No existe una cuenta con el ID solicitado")

    #Obtengo todos los movimientos de la cuenta solicitada por id
    movements = crud_movimientos.get_movementsByAccount(db, account_id)
    totalARS = 0
    totalUSD = 0

    #Filtro la lista de movimientos, sumando y restando segun corresponda para obtener el saldo total en ARS
    if movements is not None:
        for i in range(len(movements)):
            if movements[i].tipo == 1:
                totalARS += movements[i].importe #Ingreso
            else: 
                totalARS -= movements[i].importe #Egreso
        
        totalUSD = get_total_usd(totalARS) #Llamo al metodo que me va a obtener el valor en USD segun la cotización solicitada

    clientBalance = schema.CuentaSaldo(saldo_ARS= totalARS, saldo_USD= totalUSD) #Armo el objeto que va a ser mostrado en la URL
    return clientBalance

def get_total_usd(totalARS: float):
    usd_value = 0

    response_API = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales')
    data = response_API.json() #Accedo a todo el array que contiene la api en formato json para poder trabaharlo
    
    #Busco el objeto dentro de la lista data con nombre = Dolar Bolsa
    cont = 0
    encontrado = False
   
    while encontrado is False and cont < len(data):
        if data[cont]["casa"]["nombre"] == "Dolar Bolsa":
            encontrado = True
            usd_value = data[cont]["casa"]["venta"] #Me guardo la cotizacion de venta en una variable

        cont+=1

    #Formateando usd_value que llega como string con coma para poder transformarlo a floaT
    float_usd = usd_value.replace(",", ".")
    #print("USD" , float_usd)

    #Multiplico total obtenido en pesos por la cotizacion dolar venta de Dolar Bolsa
    totalUSD = totalARS * float(float_usd)
    return totalUSD