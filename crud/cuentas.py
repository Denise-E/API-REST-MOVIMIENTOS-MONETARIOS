from sqlalchemy.orm import Session
import models.Cuenta as model
from schemas import CuentaSchema as schema
from crud import movimientos as crud_movimientos


def get_accountsByClient(db: Session,client_id: int):
    return db.query(model.Cuenta).filter(model.Cuenta.id_cliente == client_id).all()

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

#Por id_cuenta tengo que obtener todos los movimientos.
#Filtro la lista de movimientos y si tipo = 1 SUMO, si tipo = 2 RESTO. 
#Rdo lo guardo en saldo_ARS
#Consumo API y lo aplico al saldo_ARS para obtener saldo_USD 
def get_clientBalance(db: Session, account_id: int):
    movements = crud_movimientos.get_movementsByAccount(db, account_id)
    totalARS = 0
    totalUSD = 0

    if movements is not None:
        for i in range(len(movements)):
            if movements[i].tipo == 1:
                totalARS += movements[i].importe
            else:
                totalARS -= movements[i].importe
        
        totalUSD = 20

    clientBalance = schema.CuentaSaldo(saldo_ARS= totalARS, saldo_USD= totalUSD)

    return clientBalance