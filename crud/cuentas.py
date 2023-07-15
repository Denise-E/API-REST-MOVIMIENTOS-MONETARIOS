from sqlalchemy.orm import Session
import models.Cuenta as model


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