from fastapi import HTTPException
from sqlalchemy.orm import Session

import models.Movimiento as model
import models.Tipo_Movimiento as model_movementsTypes
from schemas import MovimientoSchema as schema
from crud import cuentas as crud_accounts
from crud import gral_validations as validations

'''
Busco movimiento por id en la base de datos. 
Devuelve un único registro o None si no encuentra movimiento con el id solicitado
'''
def get_mov(db: Session, mov_id: int):
    return db.query(model.Movimiento).filter(model.Movimiento.id == mov_id).first()

'''
Busco todos los movimientos asociados a una misma cuenta, de la cual recibo el id. 
Devuelve una lista con los resultados o None si no encuentra ningun movimiento asociado a la cuenta
'''
def get_movementsByAccount(db: Session, account_id: int):
    return db.query(model.Movimiento).filter(model.Movimiento.id_cuenta == account_id).all()

'''
Creación de un movimiento, Ingreso o Egreso de dinero. 
Creando el registro en la base de datos en la tabla "movimientos" en caso de corresponder.
Todo ingreso se registra y en caso de los egresos solo si alcanza el saldo en la cuenta del cliente.
'''
def create_mov(db: Session, data:schema.MovimientoCreate):
    #Valido en caso que quieran hacer un egreso que alcance el saldo de la cuenta
    verificateMovementType(db, data.tipo)
    if data.tipo == 2:
        saldo = crud_accounts.get_clientBalance(db, data.id_cuenta) #Rutilizo el metodo ya creado
        saldo = saldo.saldo_ARS

        if (saldo - data.importe) < 0: #Si no alcanza para retirar el monto deciado lanzo Excepción con status 404
            raise HTTPException(status_code=404, detail="Saldo insuficiente")

    #Si alcanzó el saldo para el egreso o estan solicitando un ingreso valido los datos 
    validations.validate_movement_mount(data.importe)
    validations.validate_movement_date(data.fecha)
    account = crud_accounts.get_accountById(data.id_cuenta)

    if account is None:
        raise HTTPException(status_code=404, detail="Ingrese un id de cuenta valido")

    # Con los datos validados creo el registro.
    new_mov = model.Movimiento(id_cuenta = data.id_cuenta, tipo = data.tipo, importe = data.importe, fecha = data.fecha)
    db.add(new_mov)
    db.commit()
    db.refresh(new_mov)
    return new_mov

#Eliminación de un movimiento segun su id
def delete_mov(db: Session, mov_id: int):
    mov = get_mov(db, mov_id=mov_id) #Verifico que exista tal movimiento

    if mov is not None: #Si se encontró un movimiento con el id solicitado lo elimino.
        db.delete(mov)
        db.commit()

    #En caso de retornarse None se lanza una excepción desde el router    
    return mov
    
def verificateMovementType(db: Session, type_id: int):
    movementsTypes = db.query(model_movementsTypes.Tipo_Movimiento).offset(0).all()

    existsType = False
    if any(type.id == type_id for type in movementsTypes):
       existsType = True

    if existsType is False:
        raise HTTPException(status_code=404, detail="No existe el tipo de movimiento solicitado")