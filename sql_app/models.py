from sql_app.database import Base

from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150))
    cuentas = relationship('Categoria', secondary='categoria_cliente')


class Cuenta(Base):
    __tablename__ = "cuentas"

    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id"))


class Movimiento(Base):
    __tablename__ = "movimientos"  

    id = Column(Integer, primary_key=True, index=True)
    id_cuenta = Column(Integer, ForeignKey("cuentas.id"))
    tipo = Column(Integer, ForeignKey("tipo_movimiento.id"))
    importe = Column(Float)
    fecha = Column(DateTime)

class Tipo_Movimiento(Base):
    __tablename__ = "tipo_movimiento"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(7)) #Ingreso o Egreso

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    clientes = relationship('Cliente', secondary='categoria_cliente')


class Categoria_Cliente(Base):
    __tablename__ = "categoria_cliente"

    id_categoria = Column(Integer, ForeignKey("categorias.id"), primary_key=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id"), primary_key=True)