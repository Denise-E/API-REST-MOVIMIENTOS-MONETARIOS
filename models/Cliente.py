from config.database import Base
from sqlalchemy import Column,Integer, String
from sqlalchemy.orm import relationship


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    dni = Column(Integer, nullable=False) #Agregue dni para poder validar que no este ya registrado al registrarse
    nombre = Column(String(200), nullable=False)
    cuentas = relationship('Categoria', secondary='categoria_cliente',overlaps="cuentas")

