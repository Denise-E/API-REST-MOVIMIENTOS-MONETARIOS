from sqlalchemy.orm import Session
import models.Cuenta as model


def get_cuentasPorCliente(db: Session,client_id: int):
    account = db.query(model.Cuenta).filter(model.Cuenta.id_cliente == client_id).all()
    finalList = [{"IDs": []}]

    #Para acceder solo al id de la cuenta, sin mostrar el id del cliente.
    for i in range(len(account)): 
        finalList[0]["IDs"].append(account[i].id)

    return finalList 

def delete_clienteAccounts(db: Session, client_id: int):
    
    accounts = db.query(model.Cuenta).filter(model.Cuenta.id_cliente == client_id).all()

    if accounts is not None:
        for i in range(len(accounts)):
            db.delete(accounts[i])
            db.commit()

    return accounts