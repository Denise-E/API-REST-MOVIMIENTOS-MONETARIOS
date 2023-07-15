from sqlalchemy.orm import Session
import models.Cuenta as model


def get_cuentasPorCliente(db: Session,client_id: int):
    account = db.query(model.Cuenta).filter(model.Cuenta.id_cliente == client_id).all()
    finalList = [{"IDs": []}]

    #Para acceder solo al id de la cuenta, sin mostrar el id del cliente.
    for i in range(len(account)): 
        finalList[0]["IDs"].append(account[i].id)

    return finalList 