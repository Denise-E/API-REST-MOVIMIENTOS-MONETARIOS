from config.database import Base
from sqlalchemy import Column,Integer, String


class Tipo_Movimiento(Base):
    __tablename__ = "tipo_movimiento"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(7), nullable=False) #Ingreso o Egreso
